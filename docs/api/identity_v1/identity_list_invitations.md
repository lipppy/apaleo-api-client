# `list_invitations`

Returns a list of all invitations to the current account.

## Endpoint Mapping

- **Swagger UI link:** [https://identity.apaleo.com/swagger/index.html?urls.primaryName=Identity+V1](https://identity.apaleo.com/swagger/index.html?urls.primaryName=Identity+V1)
- **Section:** Invitation
- **HTTP method:** `GET`
- **Endpoint:** `/api/v1/account/invitations`
- **Full URL:** `https://identity.apaleo.com/api/v1/account/invitations`
- **Adapter:** `client.identity.v1.identity: IdentityV1IdentityAdapter`
- **Adapter method:** `list_invitations(params: InvitationListParams | None = None)`

## Parameters

`InvitationListParams` or `None` if no parameters are needed.

Params are optional, you can call `list_invitations()` without them to get all invitations for the account.

```python {title="InvitationListParams definition"}
@dataclass(frozen=True)
class InvitationListParams:
    property_id: str | None = None
```

## Returns

`InvitationList`

```python {title="InvitationList definition"}
@dataclass(frozen=True)
class InvitationList:
    invitations: list[Invitation]
```

For nested data structures, use the IDE's autocompletion to explore the available fields and types.

## Success Status Codes

- `200 OK`
- `204 No Content`

## Example Code

```python
import asyncio

from apaleoapi import ApaleoAPIClient, OAuth2ClientCredentialsProvider
from apaleoapi.apaleo.identity.v1.identity import InvitationListParams


async def main() -> None:
    token_provider = OAuth2ClientCredentialsProvider(
        client_id="your-client-id",
        client_secret="your-client-secret",
        service="Identity Invitations Example",
    )

    client = ApaleoAPIClient(token_provider=token_provider)

    params = InvitationListParams(property_id="BER")

    try:
        invitations = await client.identity.v1.identity.list_invitations(
            params=params,
        )
        print(f"Found {len(invitations.invitations)} invitation(s)")
    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
```
