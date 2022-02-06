from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

import jsonfeed as jf


# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.thoth.pub/graphql")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)


recents = gql(
"""
query recents($filter:String) {
  works(order: {field: PUBLICATION_DATE, direction: ASC}, workStatus: ACTIVE, limit: 20, filter: $filter) {
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
"""
)

# TODO: can we just receive params from the URL?
params = {"filter": "Philhellenes"}

result = client.execute(recents, variable_values=params)
print(result)

# TODO: fill out all the other fields.
def work_to_item(work) -> jf.Item: # TODO: type work
  return jf.Item(work['doi'])

feed = jf.Feed(
  "Thoth", # TODO: add query if there is some.
  home_page_url="https://thoth.pub/",
  feed_url="", # TODO: get from request
  description="Open Access books on Thoth",
  # TODO: support next_url for pagination.
  icon="https://thoth.pub/apple-icon-180x180.png",
  favicon="https://thoth.pub/favicon-96x96.png",
  items=[work_to_item(work) for work in result['works']],
)
