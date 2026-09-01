from .custom_types import InventoryResult


def print_inventory(inventory: list[InventoryResult]) -> None:
    """Print the AWS inventory in a human-readable format."""

    print("\nAWS ACCOUNT INVENTORY")

    for service_inventory in inventory:
        service = service_inventory["service"]
        resources = service_inventory["resources"]

        print(f"\n{service}")
        print(f"  Resources: {len(resources)}")

        for resource in resources:
            print(f"  - {resource['id']}")

            for key, value in resource.items():
                if key == "id":
                    continue

                label = key.replace("_", " ").title()
                print(f"    {label}: {value}")
