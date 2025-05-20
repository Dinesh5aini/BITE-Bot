from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_helper
import utils

app = FastAPI()
inprograss_orders = {}

@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()

    intent = payload["queryResult"]["intent"]["displayName"]
    parameters = payload["queryResult"]["parameters"]
    output_contexts = payload["queryResult"].get("outputContexts", [])

    session_id = utils.extract_session_id(output_contexts[0]["name"])


    intent_handler_dict = {
        "order.add -context: ongoing-order": add_to_order,
        "order.complete -context: ongoing-order": complete_order,
        "order.remove -context: ongoing-order": remove_from_order,
        "track.order -context: ongoing-order": track_order,
        "new.order" : clear_cache
    }

    return intent_handler_dict[intent](parameters, session_id)

def add_to_order(parameters: dict, session_id: str):

    food_items = parameters["food-item"]
    quantities = parameters["number"]

    if len(food_items) != len(quantities):
        fulfillment_text = "Please Specify the quantities for each food item."
    else:
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprograss_orders:
            inprograss_orders[session_id].update(new_food_dict)
        else:
            inprograss_orders[session_id] = new_food_dict
        
        order_str = utils.get_str_from_food_dict(inprograss_orders[session_id])

        fulfillment_text = f"So far, you have ordered: {order_str}. Is there anything else you would like to add?"

    return JSONResponse(
        content={
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [fulfillment_text]
                    }
                }
            ]
        }
    )

def complete_order(parameters: dict, session_id: str):
    if session_id not in inprograss_orders:
        fulfillment_text = "I'm having trouble finding your order. Could you please repeat it?"
    else:
        order = inprograss_orders[session_id]
        order_id = save_order_to_db(order)

        if order_id == -1:
            fulfillment_text = "Sorry, I couldn't save your order. Please try again."
        else:
            order_total = db_helper.get_total_order_price(order_id)
            fulfillment_text = f"Awesome. We have placed your order." \
                               f"Here is your order ID # {order_id}." \
                                 f"Your total is {order_total} which you can pay at the time of delivery." 
    
    del inprograss_orders[session_id]

    return JSONResponse(
        content={
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [fulfillment_text]
                    }
                }
            ]
        }
    )


def save_order_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()

    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(
            food_item,
            quantity,
            next_order_id,
        )

        if rcode == False:
            return -1
    
    db_helper.insert_order_tracking(
        next_order_id,
        "In Progress"
    )
    
    return int(next_order_id)

def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprograss_orders:
        fulfillment_text = "I'm having trouble finding your order. Could you please repeat it?"
    else:
        current_order = inprograss_orders[session_id]
        food_items = parameters["food-item"]

        removed_items = []
        no_such_items = []

        for item in food_items:
            if item not in current_order:
                no_such_items.append(item)
            else:
                removed_items.append(item)
                del current_order[item]
        
        fulfillment_text = []

        if len(removed_items) > 0:
            fulfillment_text.append(f'Removed {", ".join(removed_items)} from your order!')

        if len(no_such_items) > 0:
            missing_items = ', '.join(no_such_items)
            fulfillment_text.append(f"Your current order does not have {missing_items}")
        
        if len(current_order.keys()) == 0:
            fulfillment_text.append(" Your order is empty!")

        else:
            current_order_str = utils.get_str_from_food_dict(current_order)
            fulfillment_text.append(f"Your current order is: {current_order_str}.")

        return JSONResponse(
            content={
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": fulfillment_text
                        }
                    }
                ]
            }
        )

def track_order(parameters: dict, session_id: str):

    order_id = int(parameters["number"])
    order_status = db_helper.get_order_status(order_id)

    if order_status:
        text = f" The order status of order ID {order_id} is {order_status}."
    else:
        text = f"Sorry, I couldn't find the order status for order ID {order_id}."

    return JSONResponse(
        content={
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [text]
                    }
                }
            ]
        }
    )

def clear_cache(parameters: dict, session_id: str):
    if session_id in inprograss_orders:
        del inprograss_orders[session_id]
    
    return 