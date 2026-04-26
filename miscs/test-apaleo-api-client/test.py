import asyncio
import os

from dotenv import load_dotenv

from apaleoapi import ApaleoAPIClient
from apaleoapi.apaleo.identity.v1.identity import InvitationListParams
from apaleoapi.http.auth import OAuth2ClientCredentialsProvider

load_dotenv(".env.client_credentials")  # Load from specific .env file for this test

async def main() -> None:
	token_provider = OAuth2ClientCredentialsProvider(
		client_id=os.getenv("APALEO_API_CLIENT_ID"),
		client_secret=os.getenv("APALEO_API_CLIENT_SECRET"),
		service="Identity Invitations Example",
	)

	client = ApaleoAPIClient(token_provider=token_provider)

	try:
		invitations = await client.identity.v1.identity.list_invitations(
			InvitationListParams(property_id="BER"),
		)
		print(f"Found {len(invitations.invitations)} invitation(s)")
	finally:
		await client.aclose()


if __name__ == "__main__":
	asyncio.run(main())