This directory contains per-client configurations for Data Lake tables. 

Each client-specific repository contains configurations and schemas for different Data Lake tables. 

## Enabling new client in Data Lake

Enabling new client in Data Lake means creation of new client-specific repository, creation of relevant `config.yml` file and copying source definitions from `<existing-client>/sources/` .

If you want to add new client **new-client** to Data Lake, your steps should be following:

1. Create `new-client` directory:

```
mkdir new-client
```

2. Copy source configurations from one of the existing clients (for example, `ahold`) to `new-client` directory:

```
cp -R ahold/sources new-client/
```

3. Copy `config.yml` configuration from one of the existing clients (for example, `ahold`) to `new-client` directory:

```
cp ahold/config.yml new-client/config.yml
```

4. Adjust `client_id` and `dataset_id` in `new-client/config.yml`:

```
gsed -i 's/client_id: ahold/client_id: new-client/g' new-client/config.yml

gsed -i 's/dataset_id: datalake_ahold/dataset_id: datalake_new_client/g' new-client/config.yml
```

5. Commit changes and create PRs. 
