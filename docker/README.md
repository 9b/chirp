
# To build

From the Git repo root:

```
docker build --tag chirp -f docker/Dockerfile .
```


# To run

Expose it on port 9181 of the Docker machine:

```
docker run -p 9181:80/tcp --rm chirp
```


# Setup

Every registered user is automatically made admin once per second. Then
/settings page permits entry of Google account details.
