# Core API - Inventory V1

*Setup and manage properties (hotels, etc.) and all the entites in them to rent out:
Units such as rooms, parking lots, beds, meeting rooms, etc. Units can be combined into groups (single rooms, double rooms).*

<table>
  <thead>
    <tr>
      <th colspan="2" align="center" >Apaleo Core API &middot; Inventory V1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Swagger UI</b></td>
      <td><a href="https://api.apaleo.com/swagger/index.html?urls.primaryName=Inventory+V1">https://api.apaleo.com/swagger/index.html?urls.primaryName=Inventory+V1</a></td>
    </tr>
    <tr>
      <td><b>Client</b></td>
      <td><code>ApaleoAPIClient</code></td>
    </tr>
    <tr>
      <td><b>API</b></td>
      <td><code>ApaleoAPIClient.core</code></td>
    </tr>
    <tr>
      <td><b>Version</b></td>
      <td><code>ApaleoAPIClient.core.v1</code></td>
    </tr>
    <tr>
      <td><b>Resource</b></td>
      <td><code>ApaleoAPIClient.core.v1.inventory</code></td>
    </tr>
    <tr>
      <td><b>Centralized Type Imports</b></td>
      <td><code>from apaleoapi.apaleo.core.v1.inventory import ...</code></td>
    </tr>
  </tbody>
</table>

## Methods

Method-focused reference for Apaleo Core API's Inventory V1.

### Property

#### `list_properties`

Returns a list of properties with optional filters.

**Endpoint Mapping**

<code style="color: steelblue;">GET</code> <code>/inventory/v1/properties</code>

**SDK Method**

!!! info "`list_properties(self, params: PropertyListParams | None = None) -> PropertyList`"

    ```python title="Basic usage"
    params = PropertyListParams(page_size=50, page_number=1)
    properties = await client.core.v1.inventory.list_properties(params)

    print(properties.count)
    for item in properties.items:
      print(item.id, item.name)
    ```

??? tip "Concurrent pagination is supported"

    You can fetch multiple pages concurrently by setting `batch_size` and `is_concurrently=True` on `PropertyListParams`.

    ```python title="Concurrent pagination"
    params = PropertyListParams(batch_size=100, is_concurrently=True)
    properties = await client.core.v1.inventory.list_properties(params)
    print(properties.count)
    ```

#### `create_property`

Creates a new property.

**Endpoint Mapping**

<code style="color: lightseagreen;">POST</code> <code>/inventory/v1/properties</code>

**SDK Method**

!!! info "`create_property(self, payload: CreateProperty | dict[str, Any], idempotency_key: str | None = None) -> PropertyCreated`"

    ```python title="Basic usage"
    payload = {
      "code": "BER",
      "name": {"en": "Berlin Hotel"},
      "company_name": "Berlin Hotel GmbH",
      "commercial_register_entry": "HRB 123456",
      "tax_id": "DE123456789",
      "location": {
        "address_line1": "Alexanderplatz 1",
        "postal_code": "10178",
        "city": "Berlin",
        "country_code": "DE",
      },
      "time_zone": "Europe/Berlin",
      "default_check_in_time": "15:00:00",
      "default_check_out_time": "11:00:00",
      "currency_code": "EUR",
    }

    property_created = await client.core.v1.inventory.create_property(
      payload=payload,
      idempotency_key="property-ber-creation-001",
    )
    print(property_created.id)
    ```

??? tip "Idempotency is supported"

    Pass a unique `idempotency_key` for each create request to avoid duplicate property creation when retrying requests.

#### `count_properties`

Returns the total number of properties.

**Endpoint Mapping**

<code style="color: darkorange;">GET</code> <code>/inventory/v1/properties/$count</code>

**SDK Method**

!!! info "`count_properties(self) -> int`"

    ```python title="Basic usage"
    property_count = await client.core.v1.inventory.count_properties()
    print(property_count)
    ```

#### `get_property`

Returns the details for a specific property by ID.

**Endpoint Mapping**

<code style="color: cornflowerblue;">GET</code> <code>/inventory/v1/properties/{id}</code>

**SDK Method**

!!! info "`get_property(self, property_id: str, params: PropertyGetParams | None = None) -> Property`"

    ```python title="Basic usage"
    params = PropertyGetParams(languages=["en"], expand=["unitGroups"])
    property_item = await client.core.v1.inventory.get_property(
      property_id="BER",
      params=params,
    )
    print(property_item.id)
    print(property_item.name)
    ```

#### `update_property`

Updates property details by ID.

**Endpoint Mapping**

<code style="color: cyan;">PATCH</code> <code>/inventory/v1/properties/{id}</code>

**SDK Method**

!!! info "`update_property(self, property_id: str, payload: list[Operation]) -> None`"

    ```python title="Basic usage"
    payload = [
      Operation(
        op="replace",
        path="/name/en",
        value="Berlin Hotel Central",
      ),
      Operation(
        op="replace",
        path="/defaultCheckInTime",
        value="16:00:00",
      ),
    ]

    await client.core.v1.inventory.update_property(
      property_id="BER",
      payload=payload,
    )
    ```

#### `delete_property`

Deletes a property by ID.

**Endpoint Mapping**

<code style="color: crimson;">DELETE</code> <code>/inventory/v1/properties/{id}</code>

**SDK Method**

!!! info "`delete_property(self, property_id: str) -> None`"

    ```python title="Basic usage"
    await client.core.v1.inventory.delete_property(property_id="BER")
    ```

### Property Actions

### Types

#### `list_countries`

Returns a list of supported countries.

**Endpoint Mapping**

<code style="color: mediumseagreen;">GET</code> <code>/inventory/v1/types/countries</code>

**SDK Method**

!!! info "`list_countries(self) -> CountryList`"

    ```python title="Basic usage"
    countries = await client.core.v1.inventory.list_countries()
    print(countries.count)
    print(countries.items[:5])
    ```

### Unit

### Unit Actions

### Unit Attribute

### Unit Group

## Models and Data Structures
