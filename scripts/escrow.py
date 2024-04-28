from cryptoconditions import PreimageSha256
from dotenv import load_dotenv
import json
import websocket
import time
import os


def gen_condition_and_fulfillment():
    fulfillment_secret = os.urandom(32)

    print(f"Fulfillment secret: {fulfillment_secret.hex().upper()}")

    # Generate a condition and fulfillment
    fulfillment = PreimageSha256(preimage=fulfillment_secret)

    condition = fulfillment.condition_binary.hex().upper()
    print("Condition", condition)

    # Keep secret until you want to finish the escrow
    fulfillment = fulfillment.serialize_binary().hex().upper()
    print("Fulfillment", fulfillment)

    return fulfillment_secret, condition, fulfillment


def calc_release_or_cancel_time():
    ripple_offset = 946684800
    cancel_after = int(time.time()) + (24 * 60 * 60) - ripple_offset
    print(f"Cancelling after {cancel_after} seconds (24 hours) from now")

    return cancel_after


def create_escrow(ripple_websocket,
                  secret,
                  condition,
                  cancel_after,
                  PerformingRighthsOrganisation_account,
                  beneficiary,
                  incomeBeneficiary):
    # Set up the request object

    # Amount set in XRP drops, where 1 XRP = 1,000,000 drops.
    # https://xrpl.org/basic-data-types.html#specifying-currency-amounts
    request = {
        "id": 1,
        "command": "submit",
        "secret": secret,
        "tx_json": {
            "Account": PerformingRighthsOrganisation_account,
            "TransactionType": "EscrowCreate",
            "Amount": str(incomeBeneficiary),  # 10 XRP
            "Destination": beneficiary,
            "Condition": condition,
            "CancelAfter": cancel_after
        }
    }
    # Convert the request to a JSON string
    request_json = json.dumps(request)
    # Set up the WebSocket connection

    ws = websocket.WebSocket()
    ws.connect(ripple_websocket)  # Replace with the WebSocket URL

    # Send the request and print the response
    ws.send(request_json)
    response = ws.recv()

    print(response)

    # Close the WebSocket connection
    ws.close()

    return response


def confirm_transaction(ripple_websocket, transaction):
    # Set up the request object
    request = {
        "id": 1,
        "command": "tx",
        "transaction": transaction,
        "binary": False
    }

    # Convert the request to a JSON string
    request_json = json.dumps(request)

    # Set up the WebSocket connection
    ws = websocket.WebSocket()
    ws.connect(ripple_websocket)  # Replace with the WebSocket URL

    # Send the request and print the response
    ws.send(request_json)
    response = ws.recv()

    print(response)
    # Close the WebSocket connection
    ws.close()

    return response


def escrow_finish(ripple_websocket, PerformingRighthsOrganisation_account, secret, condition, fulfillment, sequence):
    # Set up the request object
    request = {
        "id": 1,
        "command": "submit",
        "secret": secret,
        "tx_json": {
            "Account": PerformingRighthsOrganisation_account,
            "TransactionType": "EscrowFinish",
            "Owner": PerformingRighthsOrganisation_account,
            "OfferSequence": int(sequence),
            "Condition": condition,
            "Fulfillment": fulfillment,
            "Fee": "500"
        }
    }

    # Convert the request to a JSON string
    request_json = json.dumps(request)

    # Set up the WebSocket connection
    ws = websocket.WebSocket()
    ws.connect(ripple_websocket)  # Replace with the WebSocket URL

    # Send the request and print the response
    ws.send(request_json)
    response = ws.recv()

    print(response)
    # Close the WebSocket connection
    ws.close()

    return response


def main():
    load_dotenv()

    secret = os.environ.get("SECRET_RIPPLE")
    secret_destination = os.environ.get("SECRET_RIPPLE_DEST")

    # Create a transaction to create the escrow
    # https://xrpl.org/xrp-testnet-faucet.html
    ripple_test_rpc = "https://s.altnet.rippletest.net:51234/"
    ripple_test_websocket = "wss://s.altnet.rippletest.net:51233/"
    rippled_dev_websocket = "wss://s.devnet.rippletest.net:51233/"

    with open('./metadata/bindings.json') as f:
        accounts = json.load(f)

    # Convert accounts to tuple
    accounts = tuple(accounts.values())
    PerformingRighthsOrganisation_account = "r4iTMtAQG8M89Apq5sf81GFhxwWKxPJFDD"

    # Amount set in XRP drops, where 1 XRP = 1,000,000 drops.
    amount_to_distribute = "100"  # 100 XRP
    conversion_factor = 1000000

    Beneficiaries = {
        accounts[2]: 0.3,
        accounts[4]: 0.05,
        accounts[5]: 0.5,
        accounts[3]: 0.05,
        accounts[6]: 0.1,
    }

    escrowBeneficiaries = {}

    for beneficiary, percentage in Beneficiaries.items():
        incomeBeneficiary = int(int(amount_to_distribute) * conversion_factor * percentage)

        cancel_after = calc_release_or_cancel_time()
        fulfillment_secret, condition, fulfillment = gen_condition_and_fulfillment()

        print(f"Going to create the escrow for {beneficiary} with {incomeBeneficiary} XRP")
        resp_escrow_create = create_escrow(rippled_dev_websocket,
                                           secret,
                                           condition,
                                           cancel_after,
                                           PerformingRighthsOrganisation_account,
                                           beneficiary,
                                           incomeBeneficiary)

        resp_escrow_create = json.loads(resp_escrow_create)
        txt_identity_hash = resp_escrow_create["result"]["tx_json"]["hash"]
        sequence = resp_escrow_create["result"]["tx_json"]["Sequence"]
        # txt_identity_hash = "AC0770DEF306E773E350CC3567761D4A33FDA71A0F38BAFC97DC9230E4297CA8"

        print("Waiting for the transaction to be confirmed...")
        # time.sleep(5)
        resp_confirm = confirm_transaction(rippled_dev_websocket, txt_identity_hash)

        # Save the escrow information needed to finish the escrow later
        escrowBeneficiaries[beneficiary] = {
            "condition": condition,
            "fulfillment": fulfillment,
            "sequence": sequence
        }

    print("Going to finish the escrows")

    for beneficiary, escrow_info in escrowBeneficiaries.items():

        # condition = "A0258020B1D9EFFC90CF9D6AC489643098DA99CDCDC00F9495080F80DD02E68C45AF7658810120"
        # fulfillment_secret = "A02280206BB689AD3CA99F30632140FC2FC87C55B988563772A13DA2743E5FBA40531BCD"
        # fulfillment = "A02280206BB689AD3CA99F30632140FC2FC87C55B988563772A13DA2743E5FBA40531BCD"
        # sequence = 26995994
        resp_escrow_finish = escrow_finish(rippled_dev_websocket,
                                           PerformingRighthsOrganisation_account,
                                           secret,
                                           escrow_info["condition"],
                                           escrow_info["fulfillment"],
                                           escrow_info["sequence"])

        print("Waiting for the transaction to be confirmed...")
        # time.sleep(5)
        resp_escrow_finish = json.loads(resp_escrow_finish)
        if resp_escrow_finish["status"] == "success":
            txt_identity_hash = resp_escrow_finish["result"]["tx_json"]["hash"]
            resp_confirm = confirm_transaction(rippled_dev_websocket, txt_identity_hash)

            print("Done!")


if __name__ == "__main__":
    main()
