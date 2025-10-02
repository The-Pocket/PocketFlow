from async_flow import *
from pocketflow import Flow, AsyncParallelBatchNode, Node

# Create node instances
validate_payment = ValidatePayment()
process_payment = ProcessPayment()
payment_confirmation = PaymentConfirmation()

check_stock = CheckStock()
reserve_items = ReserveItems()
update_inventory = UpdateInventory()

create_label = CreateLabel()
assign_carrier = AssignCarrier()
schedule_pickup = SchedulePickup()

# Payment processing sub-flow
validate_payment >> process_payment
validate_payment - "out_of_stock" >> validate_payment  # 循环重试
process_payment - 'something fail' >> validate_payment
process_payment - 'pass' >> payment_confirmation
payment_flow = AsyncFlow(start=validate_payment)

# Inventory sub-flow
check_stock >> reserve_items >> update_inventory
inventory_flow = AsyncFlow(start=check_stock)

# Shipping sub-flow
create_label >> assign_carrier >> schedule_pickup
shipping_flow = AsyncFlow(start=create_label)

# Connect the flows into a main order pipeline
payment_flow >> inventory_flow >> shipping_flow
# payment_flow >> inventory_flow >> create_label
# payment_flow >> inventory_flow >> assign_carrier


# Create the master flow
class OrderFlow(AsyncFlow):
    pass

order_pipeline = OrderFlow(start=payment_flow)

# Create shared data structure
shared_data = {
    "order_id": "ORD-12345",
    "customer": "John Doe",
    "items": [
        {"id": "ITEM-001", "name": "Smartphone", "price": 999.99, "quantity": 1},
        {"id": "ITEM-002", "name": "Phone case", "price": 29.99, "quantity": 1},
    ],
    "shipping_address": {
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip": "12345",
    },
}


# Run the entire pipeline asynchronously
async def main():
    await order_pipeline.run_async(shared_data)

    # Print final status
    print("\nOrder processing completed!")
    print(f"Payment: {shared_data.get('payment_confirmation')}")
    print(f"Inventory: {shared_data.get('inventory_update')}")
    print(f"Shipping: {shared_data.get('pickup_status')}")


if __name__ == "__main__":
    asyncio.run(main())
