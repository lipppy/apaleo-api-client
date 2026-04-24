# Makefile for generating Python models from OpenAPI specifications
PWD := $(shell pwd)

# Download the Swagger specification for inventory and convert it to both BaseModel and dataclass formats.
# The URL for the Swagger JSON should be specified in the Make command as an argument, for example:
# make download-swagger-json URL=https://example.com/path/to/swagger.json NAME=some_name
download-swagger-json:
	@echo "Downloading Swagger specification for inventory..."
	@if [ -z "$(URL)" ]; then \
		echo "Error: URL variable is not set. Please provide the URL of the Swagger JSON." >&2; \
		exit 1; \
	fi
	@if [ -z "$(NAME)" ]; then \
		echo "Error: NAME variable is not set. Please provide the name for the downloaded Swagger JSON file (without extension)." >&2; \
		exit 1; \
	fi
	curl -o $(PWD)/swagger_jsons/$(NAME).json $(URL)
	@echo "Download completed: $(NAME)"

convert-swagger-to-openapi:
	@echo "Converting Swagger JSON to OpenAPI format..."
	@if [ -z "$(NAME)" ]; then \
		echo "Error: NAME variable is not set. Please provide the name of the Swagger JSON file (without extension)." >&2; \
		exit 1; \
	fi
	swagger2openapi $(PWD)/swagger_jsons/$(NAME).json --outfile $(PWD)/openapi_jsons/$(NAME).json
	@echo "Conversion to OpenAPI format completed."


convert-openapi-to-base-model:
	@echo "Converting OpenAPI JSON to BaseModel format..."
	@if [ -z "$(NAME)" ]; then \
		echo "Error: NAME variable is not set. Please provide the name of the OpenAPI JSON file (without extension)." >&2; \
		exit 1; \
	fi
	poetry run datamodel-codegen \
		--input $(PWD)/openapi_jsons/$(NAME).json \
		--output $(PWD)/basemodels/$(NAME).py \
		--input-file-type openapi \
		--openapi-scopes schemas \
		--output-model-type pydantic_v2.BaseModel \
		--target-python-version 3.12 \
		--use-union-operator \
		--use-standard-collections \
		--field-constraints \
		--snake-case-field \
		--allow-population-by-field-name \
		--frozen-dataclasses \
		--reuse-model \
		--collapse-root-models \
		--formatters ruff-check ruff-format
	@echo "Conversion to base model completed."

convert-openapi-to-dataclass:
	@echo "Converting OpenAPI JSON to dataclass format..."
	@if [ -z "$(NAME)" ]; then \
		echo "Error: NAME variable is not set. Please provide the name of the OpenAPI JSON file (without extension)." >&2; \
		exit 1; \
	fi
	poetry run datamodel-codegen \
		--input $(PWD)/openapi_jsons/$(NAME).json \
		--output $(PWD)/dataclasses/$(NAME).py \
		--input-file-type openapi \
		--openapi-scopes schemas \
		--output-model-type dataclasses.dataclass \
		--target-python-version 3.12 \
		--use-union-operator \
		--use-standard-collections \
		--field-constraints \
		--snake-case-field \
		--allow-population-by-field-name \
		--frozen-dataclasses \
		--reuse-model \
		--collapse-root-models \
		--formatters ruff-check ruff-format
	@echo "Conversion to dataclass completed."

convert:
	@echo "Starting conversion process..."
	make download-swagger-json URL=$(URL) NAME=$(NAME)
	make convert-swagger-to-openapi NAME=$(NAME)
	make convert-openapi-to-base-model NAME=$(NAME)
	make convert-openapi-to-dataclass NAME=$(NAME)
	@echo "All conversions completed."

# convert-openapi-python:
# 	@echo "Starting conversion process for OpenAPI JSON..."
# 	poetry run openapi-client-python --spec swagger_jsons/$(NAME).json --output ./generated --service-name $(NAME)

# 	@echo "All conversions for OpenAPI JSON completed."

convert-openapi-python:
	@echo "Starting conversion process for OpenAPI JSON..."
	poetry run openapi-python-generator swagger_jsons/$(NAME).json ./generated_o --library httpx
	@echo "All conversions for OpenAPI JSON completed."
