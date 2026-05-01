# Identity API - Identity V1

*Manage invitations, roles, and users within the identity system.*

<table>
  <thead>
    <tr>
      <th colspan="2" align="center" >Apaleo Identity API &middot; Identity V1</th>
    </tr>
  </thead>
  <tbody>
  <tr>
    <td><b>Swagger UI</b></td>
    <td><a href="https://identity.apaleo.com/swagger/index.html?urls.primaryName=Identity+V1">https://identity.apaleo.com/swagger/index.html?urls.primaryName=Identity+V1</a></td>
  </tr>
  <tr>
    <td><b>Client</b></td>
    <td><code>ApaleoAPIClient</code></td>
  </tr>
  <tr>
    <td><b>API</b></td>
    <td><code>ApaleoAPIClient.identity</code></td>
  </tr>
  <tr>
    <td><b>Version</b></td>
    <td><code>ApaleoAPIClient.identity.v1</code></td>
  </tr>
  <tr>
    <td><b>Resource</b></td>
    <td><code>ApaleoAPIClient.identity.v1.identity</code></td>
  </tr>
  </tbody>
</table>

## Methods

Method-focused reference for Apaleo Identity API's Identity V1.

### Invitation

#### `list_invitations`

Returns a list of all invitations to the current account.

**Endpoint Mapping**

<code style="color: skyblue;">GET</code> <code>/api/v1/invitations</code>

**SDK Method**

!!! info "`list_invitations(params: InvitationListParams | dict[str, Any] | None = None) -> InvitationList`"

    ```python {title="Without parameters"}
    # Without parameters
    invitations = await client.identity.v1.identity.list_invitations()
    print(invitations)
    ```

    ```python {title="With parameters"}
    # With parameters
    params = InvitationListParams(property_id="BER")
    invitations = await client.identity.v1.identity.list_invitations(params)
    print(invitations)

    ```

    ```python {title="With parameters as a dict"}
    params = {"property_id": "BER"} # or {"propertyId": "BER"}
    invitations = await client.identity.v1.identity.list_invitations(params)
    print(invitations)
    ```

#### `create_invitation`

Invites a person to the current account with the requested roles and properties.

**Endpoint Mapping**

<code style="color: lightseagreen;">POST</code> <code>/api/v1/invitations</code>

**SDK Method**

!!! info "`create_invitation(payload: CreateInvitation | dict[str, Any]) -> InvitedUserToAccountResponse`"

    ```python
    payload = CreateInvitation(
        email="james.twelvetrees@invalid.com",
        properties=["BER"],
        is_account_admin=False,
        role=RoleInvitedTo.HOUSEKEEPING,
    )
    invited_user = await client.identity.v1.identity.create_invitation(payload=payload)
    print(invited_user)
    ```

    ```python {title="With payload as a dict"}
    payload = {
      "email": "james.twelvetrees@invalid.com",
      "properties": ["BER"],
      "is_account_admin": False,
      "role": "Housekeeping",
    }
    invited_user = await client.identity.v1.identity.create_invitation(payload=payload)
    print(invited_user)
    ```

#### `delete_invitation`

Deletes an invitation by email.

**Endpoint Mapping**

<code style="color: crimson;">DELETE</code> <code>/api/v1/invitations/<span style="color: mediumpurple;">{email}</span></code>

**SDK Method**

!!! info "`delete_invitation(email: str) -> None`"

    ```python
    await client.identity.v1.identity.delete_invitation(email="james.twelvetrees@invalid.com")
    ```

### Roles

#### `list_roles`

Returns a list of all roles in the current account.

**Endpoint Mapping**

<code style="color: skyblue;">GET</code> <code>/api/v1/roles</code>

**SDK Method**

!!! info "`list_roles() -> RoleList`"

    ```python
    roles = await client.identity.v1.identity.list_roles()
    print(roles)
    ```

### Users

#### `list_users`

Returns a list of all users that have access to the current account.

**Endpoint Mapping**

<code style="color: skyblue;">GET</code> <code>/api/v1/users</code>

**SDK Method**

!!! note "`list_users(self, params: UserListParams | dict[str, Any] | None = None) -> UsersList`"

    ```python {title="Without parameters"}
    users = await client.identity.v1.identity.list_users()
    print(users)
    ```

    ```python {title="With parameters, paginated"}
    params = UserListParams(property_ids=["BER", "VIE"], page_size=50, page_number=1)
    users = await client.identity.v1.identity.list_users(params)
    print(users)
    ```

    ```python {title="With parameters as a dict"}
    params = {"property_ids": ["BER", "VIE"], "page_size": 50, "page_number": 1}
    users = await client.identity.v1.identity.list_users(params)
    print(users)
    ```

??? tip "Concurrent data fetching is supported"

    Concurrent pagination is supported for `list_users`. You can fetch multiple pages of results concurrently by passing `batch_size` and `is_concurrently=True` in the parameters.

    ```python
    params = UserListParams(batch_size=50, is_concurrently=True)
    users = await client.identity.v1.identity.list_users(params)
    print(users)
    ```

#### `get_user`

Returns a user in the current account for a specific `subjectId`.

**Endpoint Mapping**

<code style="color: skyblue;">GET</code> <code>/api/v1/identity/users/<span style="color: mediumpurple;">{subjectId}</span></code>

**SDK Method**

!!! info "`get_user(user_id: str) -> User`"

    ```python
    user = await client.identity.v1.identity.get_user(user_id="some_subject_id")
    print(user)
    ```

#### `update_user`

Modify user in an account.

**Endpoint Mapping**

<code style="color: cyan;">PATCH</code> <code>/api/v1/identity/users/<span style="color: mediumpurple;">{subjectId}</span></code>

**SDK Method**

!!! info "`update_user(self, user_id: str, payload: list[Operation] | list[dict[str, Any]]) -> None`"

    ```python
    payload = [
        Operation(
            op="replace",
            path="/enabled",
            value=True,
        ),
        Operation(
            op="add",
            path="/properties",
            value=["BER", "VIE"],
        ),
    ]
    await client.identity.v1.identity.update_user(
        user_id="some_subject_id",
        payload=payload,
    )
    ```

    ```python {title="With patch payload as a list of dicts"}
    payload = [
        {
            "op": "replace",
            "path": "/enabled",
            "value": True,
        },
        {
            "op": "add",
            "path": "/properties",
            "value": ["BER", "VIE"],
        },
    ]
    await client.identity.v1.identity.update_user(
        user_id="some_subject_id",
        payload=payload,
    )
    ```

#### `get_current_user`

Returns details for the current user.

It does not work with client credentials flow, as there is no user context in that case.

**Endpoint Mapping**

<code style="color: skyblue;">GET</code> <code>/api/v1/users/me</code>

**SDK Method**

!!! info "`get_current_user() -> User`"

    ```python
    current_user = await client.identity.v1.identity.get_current_user()
    print(current_user)
    ```

## Models and Data Structures
