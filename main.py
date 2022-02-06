import json
from flask import Request

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
            order: {field: PUBLICATION_DATE, direction: ASC},
            workStatus: ACTIVE,
            limit: $limit,
            filter: $filter
        ) {
            workType
            fullTitle
            publicationDate
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
                contributionType
                fullName
            }
            subjects(subjectTypes:KEYWORD) {
                subjectCode
            }
        }
    }
""")


# TODO: fill out all the other fields.
def work_to_item(work: dict) -> jf.Item:
    return jf.Item(work['doi'])


def main(request: Request):
    # TODO: use logging
    print(json.dumps(dict(
        severity="INFO",
        message="Serving feed",
        request_url=request.url,
        trace_header=request.headers.get('X-Cloud-Trace-Context')
    )))
    # TODO: convert limit arg to int.
    result = client.execute(recents, variable_values=request.args)
    feed = jf.Feed(
        "Thoth",  # TODO: add query if there is some.
        home_page_url="https://thoth.pub/",
        feed_url="",  # TODO: get from request
        description="Open Access books on Thoth",
        # TODO: support next_url for pagination.
        icon="https://thoth.pub/apple-icon-180x180.png",
        favicon="https://thoth.pub/favicon-96x96.png",
        items=[work_to_item(work) for work in result['works']],
    )
    return feed.toJSON()
