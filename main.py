import json
from typing import Union
import maya
from flask import Request, Response
import functions_framework

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import jsonfeed as jf


# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.thoth.pub/graphql")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)


recents = gql("""
    query recents($filter: String, $limit: Int = 20) {
        works(
            order: {field: PUBLICATION_DATE, direction: DESC},
            workStatus: ACTIVE,
            limit: $limit,
            filter: $filter
        ) {
            workType
            fullTitle
            publicationDate
            shortAbstract
            longAbstract
            doi
            coverUrl
            landingPage
            publications(publicationTypes: [PDF, HTML, EPUB]) {
                publicationType
                locations {
                    fullTextUrl
                }
            }
            contributions {
                fullName
            }
            subjects(subjectTypes:KEYWORD) {
                subjectCode
            }
        }
    }
""")


def work_to_item(work: dict) -> jf.Item:
    publication_date = work.get('publicationDate')
    date_published = maya.parse(publication_date).rfc3339() if publication_date else None
    attachments = [to_attachment(publication) for publication in work.get('publications', [])]
    return jf.Item(
        work.get('doi'),
        url=work.get('doi'),
        title=work.get('fullTitle'),
        content_text=work.get('longAbstract'),
        summary=work.get('shortAbstract'),
        image=work.get('coverUrl'),
        banner_image=work.get('coverUrl'),
        date_published=date_published,
        authors=[jf.Author(author.get('fullName')) for author in work.get('contributions', [])],
        tags=[subject.get('subjectCode') for subject in work.get('subjects', [])],
        attachments=list(filter(None, attachments)),
    )


def to_attachment(publication: dict) -> Union[jf.Attachment, None]:
    publication_type_to_mime_type = {
        'HTML': 'text/html',
        'PDF': 'application/pdf',
        'EPUB': 'application/epub+zip',
    }
    locations = publication.get('locations')
    publication_type = publication.get('publicationType')
    if len(locations) == 0 or publication_type not in publication_type_to_mime_type:
        return None
    return jf.Attachment(
        url=locations.pop().get('fullTextUrl'),
        mime_type=publication_type_to_mime_type[publication_type]
    )


# TODO: define some logging constructor that includes the trace.


@functions_framework.http
def main(request: Request):
    print(json.dumps(dict(
        severity='INFO',
        message='Received request',
        request_url=request.url,
        trace_header=request.headers.get('X-Cloud-Trace-Context')
    )))
    # TODO: convert limit arg to int.
    result = client.execute(recents, variable_values=request.args)
    print(json.dumps(dict(
        severity='INFO',
        message='Serving feed with {} items'.format(len(result['works'])),
        request_url=request.url,
        trace_header=request.headers.get('X-Cloud-Trace-Context')
    )))

    title = 'Thoth'
    description = 'Open Access books on Thoth'
    if 'filter' in request.args:
        title = '{}: "{}"'.format(title, request.args['filter'])
        description = '{} for the filter "{}"'.format(description, request.args['filter'])

    feed = jf.Feed(
        title,
        home_page_url="https://thoth.pub/",
        feed_url=request.url,
        description=description,
        icon="https://thoth.pub/apple-icon-180x180.png",
        favicon="https://thoth.pub/favicon-96x96.png",
        items=[work_to_item(work) for work in result['works']],
    )

    return Response(feed.to_json(), content_type='application/json; charset=utf-8')
