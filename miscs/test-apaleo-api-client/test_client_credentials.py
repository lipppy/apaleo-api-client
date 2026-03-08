import argparse
import asyncio
import json
import logging
from dataclasses import asdict

from dotenv import dotenv_values

from apaleoapi import ApaleoAPIClient
from apaleoapi.apaleo.identity.v1.contracts.identity.payloads import CreateInvitation
from apaleoapi.apaleo.identity.v1.contracts.identity.queries import UserListParams
from apaleoapi.http.auth import OAuth2ClientCredentialsProvider

# Load environment variables from .env file
config = dotenv_values(".env.client_credentials")  # Load from specific .env file for this test

# Logging configuration
log_level = config.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s | %(levelname)8s | %(message)s",
)
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Test Apaleo API Client")
parser.add_argument(
    "-c",
    "--client-id",
    type=str,
    required=False,
    help="client ID for Apaleo API (can also be set via CLIENT_ID environment variable)",
)
parser.add_argument(
    "-s",
    "--client-secret",
    type=str,
    required=False,
    help="client secret for Apaleo API (can also be set via CLIENT_SECRET environment variable)",
)
parser.add_argument(
    "-d",
    "--dry-run",
    action="store_true",
    help="run in dry-run mode (no actual API calls)",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="enable verbose logging",
)
args = parser.parse_args()

# Set logging level to DEBUG if verbose flag is provided
if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)

log = logging.getLogger(__name__)


async def main() -> None:
    """Main function to test Apaleo API client."""

    client_id = args.client_id or config.get("APALEO_CLIENT_ID")
    client_secret = args.client_secret or config.get("APALEO_CLIENT_SECRET")

    if not client_id or not client_secret:
        log.error(
            "Client ID and Client Secret must be provided either via "
            "command line or environment variables."
        )
        return

    token_provider = OAuth2ClientCredentialsProvider(
        client_id=client_id,
        client_secret=client_secret,
        service="Apaleo API Client - Machine to Machine Authentication",
    )

    # Initialize the Apaleo API client with your credentials
    client = ApaleoAPIClient(
        token_provider=token_provider,
        dry_run=args.dry_run,  # Set to False to make actual API calls
    )

    log.info("Apaleo API client initialized...")
    log.info(client)

    # create_property = await client.core.v1.inventory.create_property(
    #     idempotency_key="unique-key-123",
    # )
    # print(json.dumps(asdict(create_property), indent=2, default=str))
    # return
    # # Fetch properties asynchronously
    # properties = await client.core.v1.inventory.list_properties(
    #     params=PropertyListParams(page_size=10, page_number=1)
    # )
    # print(properties)
    # properties = await client.core.v1.inventory.list_properties(
    #     params=PropertyListParams(batch_size=5)
    # )
    # print(properties)
    # properties = await client.core.v1.inventory.list_properties(
    #     params={"batch_size": 5, "is_concurrently": True}
    # )
    # print(json.dumps(asdict(properties), indent=2, default=str))
    # property_ber = await client.core.v1.inventory.get_property(property_id="BER", params={})
    # print(json.dumps(asdict(property_ber), indent=2, default=str))
    # countries = await client.core.v1.inventory.list_countries()
    # print(json.dumps(asdict(countries), indent=2, default=str))

    # property_ber = await client.core.v1.inventory.get_property(property_id="BER", params={})
    # print(json.dumps(asdict(property_ber), indent=2, default=str))

    try:
        invitations_pre = await client.identity.v1.identity.list_invitations()
        log.info(json.dumps(asdict(invitations_pre), indent=2, default=str))
    except Exception as e:
        log.error(f"Error listing invitations: {e}")
        invitations_pre = None

    if invitations_pre is None:
        log.info("No invitations found, creating invitation for gliptak.huat@gmail.com")
    elif "gliptak.huat@gmail.com" not in [inv.email for inv in invitations_pre.invitations]:
        try:
            payload = CreateInvitation(
                email="gliptak.huat@gmail.com",
                # email="gliptak.huatkukacgmail.com",
                is_account_admin=True,
            )
            invitation = await client.identity.v1.identity.create_invitation(payload=payload)
            log.info(json.dumps(asdict(invitation), indent=2, default=str))
        except Exception as e:
            log.error(f"Error creating invitation: {e}")
    else:
        log.info(invitations_pre)
        log.info("Invitation for gliptak.huat@gmail.com already exists")
        try:
            await client.identity.v1.identity.delete_invitation(email="gliptak.huat@gmail.com")
        except Exception as e:
            log.error(f"Error deleting invitation: {e}")

    roles = await client.identity.v1.identity.list_roles()
    log.info(json.dumps(asdict(roles), indent=2, default=str))

    params = UserListParams(page_size=1, page_number=1)
    users = await client.identity.v1.identity.list_users(params=params)
    log.info(json.dumps(asdict(users), indent=2, default=str))

    try:
        user = await client.identity.v1.identity.get_user(user_id="GKTN-SP-LIPPPY")
        log.info(json.dumps(asdict(user), indent=2, default=str))
    except Exception as e:
        log.error(f"Error fetching user: {e}")

    try:
        user = await client.identity.v1.identity.get_user(
            user_id="5228b520-dc67-4666-b45e-08cdaa06d8e6"
        )
        log.info(json.dumps(asdict(user), indent=2, default=str))
    except Exception as e:
        log.error(f"Error fetching user: {e}")

    try:
        user_me = await client.identity.v1.identity.get_current_user()
        log.info(json.dumps(asdict(user_me), indent=2, default=str))
    except Exception as e:
        log.error(f"Error fetching current user: {e}")

    # params = PropertyListParams(batch_size=1, is_concurrently=True)
    # properties = await client.core.v1.inventory.list_properties(params=params)
    # print(json.dumps(asdict(properties), indent=2, default=str))

    # params = PropertyListParams(batch_size=1)
    # properties = await client.core.v1.inventory.list_properties(params=params)
    # print(json.dumps(asdict(properties), indent=2, default=str))

    # Clean up resources
    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
