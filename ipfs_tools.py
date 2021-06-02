import argparse
import os
import requests
import sys

BLOCKFROST_IPFS = os.getenv('BLOCKFROST_IPFS')


def create_ipfs(image):
    """ Uploads image to IPFS using Blockfrost API """
    with open(image, "rb") as file_upload:
        ipfs_create_url = "https://ipfs.blockfrost.io/api/v0/ipfs/add"
        files = {'file': file_upload}
        headers = {"project_id": f"{BLOCKFROST_IPFS}"}
        res = requests.post(ipfs_create_url,  files=files, headers=headers)
        res.raise_for_status()
        if res.status_code == 200:
            print("Uploaded image to Blockfrost")
            print(res.json())
            return res.json()
        else:
            logger.error("Image upload failed somehow. Have you created and updated Blockfrost API key in .env?")
            return Falses

def pin_ipfs(ipfs_hash):
    """ Pins IPFS hash to Blockfrost """
    ipfs_pin_url = f"https://ipfs.blockfrost.io/api/v0/ipfs/pin/add/{ipfs_hash}"
    headers = {"project_id": f"{BLOCKFROST_IPFS}"}
    res = requests.post(ipfs_pin_url, headers=headers)
    res.raise_for_status()
    if res.status_code == 200:
        print("Pinned to Blockfrost")
        print(res.json())
        return True
    else:
        logger.error("Pin failed somehow.")
        return False


def remove_ipfs(ipfs_hash):
    """ Removes pinned IPFS hash from Blockfrost """
    ipfs_remove_url = f"https://ipfs.blockfrost.io/api/v0/ipfs/pin/remove/{ipfs_hash}"
    headers = {"project_id": f"{BLOCKFROST_IPFS}"}
    res = requests.post(ipfs_remove_url, headers=headers)
    res.raise_for_status()
    if res.status_code == 200:
        print("Remove successful")
        print(res.json())
        return True
    else:
        logger.error("Pin not removed")
        return False

def main(**kwargs):
    if kwargs.get('create_ipfs'):
        print(kwargs.get('create_ipfs'))
        res = create_ipfs(image=kwargs.get('create_ipfs'))
        if res:
            print('Created IPFS hash')

    elif kwargs.get('pin_ipfs'):
        print(kwargs.get('pin_ipfs'))
        res = pin_ipfs(ipfs_hash=kwargs.get('pin_ipfs'))
        if res:
            print('Pinned IPFS hash')

    elif kwargs.get('remove_ipfs'):
        print(kwargs.get('remove_ipfs'))
        res = remove_ipfs(ipfs_hash=kwargs.get('remove_ipfs'))
        if res:
            print('Removed IPFS hash')

    return print(' -- end --')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--create_ipfs',
        help='Create the IPFS hash',
        required=False
    )

    parser.add_argument(
        '--pin_ipfs',
        help='Pin the IPFS',
        required=False
    )

    parser.add_argument(
        '--remove_ipfs',
        help='Remove the IPFS',
        required=False
    )
    args = parser.parse_args()

    # Convert the argparse.Namespace to a dictionary: vars(args)
    arg_dict = vars(args)
    # pass dictionary to main
    main(**arg_dict)
    sys.exit(0)
