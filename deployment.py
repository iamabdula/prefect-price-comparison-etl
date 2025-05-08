from prefect import flow
from prefect.docker import DockerImage

if __name__ == "__main__":
    flow.from_source(
        "https://github.com/iamabdula/prefect-price-comparison-etl.git",
        entrypoint="etl/flow.py:etl_flow",
    ).deploy(
        name="my-custom-dockerfile-deployment",
        work_pool_name="my-work-pool",
        image=DockerImage(
            name="prefecthq/prefect:3-latest",  # Use a valid Prefect image
            dockerfile="Dockerfile",
            env={  # Set the environment variables here
                "POSTGRES_USER": "admin",
                "POSTGRES_PASSWORD": "admin",
                "POSTGRES_DB": "product_ops",
                "DATABASE_URL": "postgresql://admin:admin@etl_postgres:5432/product_ops"
            }
        ),
        push=False
    )
