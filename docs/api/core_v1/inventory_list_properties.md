# Core API - Inventory V1

Method-focused reference for Core Inventory V1.

## Method Index

| Method | Description | Request Type | Response Type |
| --- | --- | --- | --- |
| `list_properties` | List properties for the current account with optional filters and pagination. | `PropertyListParams | None` | `PropertyList` |

## `list_properties`

Returns a list of properties from the current account.

### Endpoint Mapping

- **Swagger UI link:** [https://api.apaleo.com/swagger/index.html?urls.primaryName=Inventory+V1](https://api.apaleo.com/swagger/index.html?urls.primaryName=Inventory+V1)
- **Section:** Property
- **HTTP method:** `GET`
- **Endpoint:** `/inventory/v1/properties`
- **Full URL:** `https://api.apaleo.com/inventory/v1/properties`
- **Adapter:** `client.core.v1.inventory: CoreV1InventoryAdapter`
- **Adapter method:** `list_properties(params: PropertyListParams | None = None) -> PropertyList`

### Parameters

`PropertyListParams` or `None` if no filters are needed.

All parameters are optional, so `list_properties()` is valid.

```python {title="PropertyListParams definition"}
@dataclass
class PropertyListParams(BatchRequest):
	status: list[str] | None = None
	include_archived: bool | None = None
	country_code: list[str] | None = None
	expand: list[str] | None = None


@dataclass
class BatchRequest:
	page_number: int | None = None
	page_size: int | None = None
	batch_size: int | None = None
	is_concurrently: bool | None = None
```

### Returns

`PropertyList`

```python {title="PropertyList definition"}
@dataclass
class PropertyList:
	items: list[PropertyItem]
	count: int
```

### Success Status Codes

- `200 OK`
- `204 No Content`

### Example Code

```python
import asyncio

from apaleoapi import ApaleoAPIClient, OAuth2ClientCredentialsProvider
from apaleoapi.apaleo.core.v1.dataclasses.inventory.query import PropertyListParams


async def main() -> None:
	token_provider = OAuth2ClientCredentialsProvider(
		client_id="your-client-id",
		client_secret="your-client-secret",
		service="Core Inventory Example",
	)

	client = ApaleoAPIClient(token_provider=token_provider)

	params = PropertyListParams(
		status=["Live"],
		include_archived=False,
		page_size=100,
	)

	try:
		properties = await client.core.v1.inventory.list_properties(params=params)
		print(f"Found {properties.count} properties")

		if properties.items:
			first = properties.items[0]
			print(first.id, first.name, first.location.country_code)
	finally:
		await client.aclose()


if __name__ == "__main__":
	asyncio.run(main())
```

## Model Reference (Nested Structures)

Type safety is a key SDK feature, so nested models are documented explicitly.

```python {title="PropertyItem"}
@dataclass
class PropertyItem:
	id: str
	code: str
	name: str
	company_name: str
	commercial_register_entry: str
	tax_id: str
	location: Address
	time_zone: str
	currency_code: str
	created: datetime
	status: str
	is_archived: bool

	property_template_id: str | None = None
	is_template: bool = False
	description: str | None = None
	managing_directors: str | None = None
	bank_account: BankAccount | None = None
	payment_terms: dict[str, str | None] = field(default_factory=dict)
	actions: list[Action] | None = None
```

```python {title="Address"}
@dataclass
class Address:
	address_line1: str
	postal_code: str
	city: str
	country_code: str

	address_line2: str | None = None
	region_code: str | None = None
```

```python {title="BankAccount"}
@dataclass
class BankAccount:
	iban: str | None = None
	bic: str | None = None
	bank: str | None = None
```

```python {title="Action"}
@dataclass
class Action:
	action: str
	is_allowed: bool
	reasons: list[ActionReason] | None = None


@dataclass
class ActionReason:
	code: str
	message: str
```
