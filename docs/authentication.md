---
stoplight-id: 2aq3knmc7036u
tags:
  - auth
---

# Authentication

The Navixy IoT Logic API supports two authentication methods:

1. **User session hash**: The basic authentication method obtained through user login
2. **API key**: The recommended, more secure method for ongoing API access and integrations

## 1. User session hash (basic authentication)

A session hash is the basic authentication token in the Navixy system and serves as the starting point for authentication workflows.

Use session hashes for:

* Initial system access
* User interface operations
* Short-term scripts

> Session hash limitations:
>
> * Expires after periods of inactivity (30 days)
> * Invalidated when logging out or changing password
> * Requires periodic renewal for longer sessions
> * Less secure for automated processes

### Obtaining a session hash

To get a session hash, send a POST request to the user authentication endpoint `{baseURL}/v2/user/auth` providing your account's login and passord as parameters:

```bash
curl -X POST "https://your.server.com/v2/user/auth" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "your@email.com",
    "password": "your_password"
  }'
```

Successful response:

```json
{
  "success": true,
  "hash": "22eac1c27af4be7b9d04da2ce1af111b"
}
```

Copy the `hash` parameter value and save it, you will use it for authenticating your further requests.

## 2. API keys (recommended authentication)

API keys are a more stable and secure authentication method, it is recommended for long-term use with all production integrations and automated systems. Here's a comparison with session hash to highlight API key advantages:

| Feature                  | API Keys                       | Session Hashes                        |
| ------------------------ | ------------------------------ | ------------------------------------- |
| Expiration               | Don't automatically expire     | Expire after 30 days                  |
| Password changes         | Not affected                   | Immediately invalidated               |
| User logout              | Not affected                   | Immediately invalidated               |
| Credential storage       | Only store the API key         | Must store/access username & password |
| Revocation               | Individual keys can be revoked | All sessions terminated together      |
| Integration segmentation | One key per integration        | All use same credentials              |
| Periodic renewal         | Not required                   | Required for long sessions            |

> API key limitations:
>
> * Every user account may have up to 20 API keys
> * Only account Owners have access to API keys functionality

### Creating API keys

API keys should be created through the Navixy web interface:

1. **Login to the Web Interface**:
   * Access the Navixy user interface via the web.
   * Use your credentials to log in.
2. **Navigate to the API Key Section**:
   * Once logged in, click on your username.
   * Find and select the `API Keys` section.
3. **Generate a New API Key**:
   * Click on the plus button on the top left corner.
   * Provide a name for the API key to easily identify it later.
   * Click `Save`.
4. **Copy the API Key Hash**:
   * Once the key is generated, you will see it in the API keys table, including the label, creation date, and the API key hash.
   * Use this hash in your API requests.

## Using authentication in API requests

You can include your authentication credentials in requests through three different methods. Each method has specific use cases and security considerations.

### 1. As a request header (recommended)

Include the hash in the `Authorization` header

{% tabs %}
{% tab title="Example" %}
```
Authorization: NVX your_hash_or_api_key
```
{% endtab %}

{% tab title="Valid" %}
```
Authorization: NVX 22eac1c27af4be7b9d04da2ce1af111b
```
{% endtab %}

{% tab title="Invalid" %}
```
# missing space after NVX
```
{% endtab %}
{% endtabs %}

This is the most secure method and follows API best practices. It keeps authentication separate from request data and works well with all HTTP methods.

### 2. In the request body

Include your authentication directly in the JSON body of your request as the`hash` parameter:

```json
{
  "hash": "your_hash_or_api_key",
  "param1": "value1"
}
```

This method works only with POST requests and mixes authentication with request parameters. It can be useful for testing but is less ideal for production use.

### 3. As a query parameter (testing only)

Append your authentication `hash`to the URL as a query parameter:

```
https://api.navixy.com/v2/iot/logic/flow/list?hash=your_hash_or_api_key
```

{% hint style="danger" %}
This method is for testing purposes only as it exposes your authentication credentials in URLs, server logs, and browser history. Never use this method in production environments.
{% endhint %}

## Managing API keys

These endpoints allow you to manage your API keys through the API itself using a valid session hash.

### Listing API keys

Get a complete list of all API keys associated with your account:

```bash
curl -X POST "https://api.eu.navixy.com/v2/user/api_key/list" \
  -H "Content-Type: application/json" \
  -d '{
    "hash": "your_session_hash"
  }'
```

This endpoint returns all your active API keys with their labels and creation dates, helping you manage and audit your integrations.

### Deleting an API key

Immediately revoke an API key when it's no longer needed or if it may have been compromised:

```bash
curl -X POST "https://api.eu.navixy.com/v2/user/api_key/delete" \
  -H "Content-Type: application/json" \
  -d '{
    "hash": "your_session_hash",
    "api_key": "api_key_to_delete"
  }'
```

Any application using this key will immediately lose access and need to be reconfigured with a new key.

## Recommended authentication flow

After understanding the available authentication methods, follow this recommended progression for integrating with the Navixy IoT Logic API:

1. **Initial authentication**
   * Authenticate with username/password to obtain a session hash
   * This step is mandatory and cannot be skipped
   * Session hashes provide temporary access needed to create API keys
2. **API key creation**
   * Use the session hash to create one or more API keys
   * Create separate API keys for different integrations
   * Give each key a descriptive name to identify its purpose
3. **Ongoing API access**
   * Use API keys for all subsequent API calls
   * Store API keys securely in your integration
   * Implement the API key in headers for maximum security
4. **API key management**
   * Periodically rotate API keys for security
   * Revoke compromised or unused API keys
   * Monitor key usage for unusual patterns

## Authentication errors

Understanding authentication errors helps you troubleshoot issues and implement proper error handling in your integration:

```json
{
  "success": false,
  "status": {
    "code": 3,
    "description": "Access denied"
  }
}
```

Common authentication error codes:

* **Code 3: Wrong hash** - Your API key or session hash is invalid or has been revoked
* **Code 4: User or API key not found or session ended** - User or session hash don't exist or expired
* **Code 7: Invalid parameters** - Inserted request parameters are incorrect

Your integration should handle these errors appropriately, possibly by prompting for re-authentication or alerting administrators about potential issues.

## Best practices

1. **Log in to the needed Navixy account** to access the system initially - **Owner** account role is needed
2. **Create and use API keys** for all ongoing integration needs - they provide more stable, secure access
3. **Use separate keys** for different integrations for better management and security isolation
4. **Add descriptive labels** to easily identify the purpose of each key when viewing your key list
5. **Revoke compromised keys** promptly to maintain security of your account
6. **Transmit authentication credentials** only over HTTPS to prevent interception of keys
7. **Store credentials securely** server-side, never in client-side code or public repositories
8. **Implement proper error handling** for authentication failures, including automatic recovery where appropriate
