# Contributing

You should be using an IDE, otherwise start there...

Formatting (this is done by you):

- Black (.py)
- Prettier (.yml;.yaml;.json;.md)

Linting (this is checked by actions):

- Flake8 (.py)
- ShellCheck (.sh)

## Running Locally

1. Install `act`: https://nektosact.com/installation/index.html
2. Create a `.secrets` file with: `CLOUDFLARE_API_TOKEN="xxx"`
3. Run `act -j test --env DOMAINS=example.com` with your domain!

The test updates the [action.yml](action.yml) to use the [Dockerfile](src/Dockerfile).
This ensures the test will always use your local changes.

To test the docker image, run: [build.sh](build.sh)

To see all available jobs run: `act -l`
