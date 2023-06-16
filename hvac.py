import hvac

# Azure Service Principal credentials
tenant_id = "<your_tenant_id>"
client_id = "<your_client_id>"
client_secret = "<your_client_secret>"

# Vault connection details
vault_url = "<your_vault_url>"
vault_secret_path = "secret/myapp/mysecret"

# Authenticate using Azure Service Principal
client = hvac.Client(url=vault_url)
client.auth.azure.login(
    role="reader",
    jwt=f"{{\"tenant_id\": \"{tenant_id}\", \"client_id\": \"{client_id}\", \"client_secret\": \"{client_secret}\"}}"
)

# Fetch the secret from Vault
secret = client.secrets.kv.v2.read_secret_version(path=vault_secret_path)

# Extract the secret value
secret_value = secret["data"]["data"]["value"]
print("Secret value:", secret_value)
