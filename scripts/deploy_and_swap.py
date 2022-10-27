from distutils.command.config import config
from scripts.helpful_scripts import get_account, get_contract_address, get_ABI
from brownie import UniswapV2Swap, network, web3
import time
from web3 import Web3
import json


def deploy():
    account = get_account()
    testContract = UniswapV2Swap.deploy({"from": account})
    time.sleep(1)
    return testContract


def swap(testContract, tokenOutAddress, amountMinOut, amountIn, token2):
    account = get_account()
    w3 = Web3()
    ABI = get_ABI(token2)
    token = w3.eth.contract(
        address=str(tokenOutAddress),
        abi=ABI,
    )
    token_balance = token.functions.balanceOf(account.address).call()
    print("Starting ETH Balance")
    print(web3.fromWei(w3.eth.get_balance(account.address), "ether"))
    print("Starting DAI Balance")
    print(web3.fromWei(token_balance, "ether"))

    tx = testContract.swap(
        tokenOutAddress,
        amountMinOut,
        account.address,
        {"from": account, "value": amountIn},
    )
    tx.wait(1)

    token_balance = token.functions.balanceOf(account.address).call()
    print("Ending ETH Balance")
    print(web3.fromWei(w3.eth.get_balance(account.address), "ether"))
    print("Ending DAI Balance")
    print(web3.fromWei(token_balance, "ether"))


def setRouter(testContract, router):
    account = get_account()
    tx = testContract.setRouter(router, {"from": account})
    tx.wait(1)


def setWETH(testContract, weth):
    account = get_account()
    tx = testContract.setWETH(weth, {"from": account})
    tx.wait(1)


def getAddresses(router, weth, token_out):
    ROUTER = get_contract_address(router)
    WETH = get_contract_address(weth)
    TOKEN_OUT = get_contract_address(token_out)
    return ROUTER, WETH, TOKEN_OUT


def printParameters(token1, token2, AMOUNT_IN):
    print(
        "\n"
        + "Swap Parameters:"
        + "\n"
        + "Token In: "
        + token1
        + "\n"
        + "Token Out: "
        + token2
        + "\n"
        + "Amount In: "
        + str(web3.fromWei(AMOUNT_IN, "ether"))
        + "\n"
    )


def main():
    AMOUNT_OUT_MIN = 100
    AMOUNT_IN = web3.toWei(0.01, "ether")
    token1 = "weth"
    token2 = "dai"
    ROUTER, WETH, TOKEN_OUT = getAddresses("uniswap_router_v2", token1, token2)
    printParameters(token1, token2, AMOUNT_IN)

    testContract = deploy()
    setRouter(testContract, ROUTER)
    setWETH(testContract, WETH)
    swap(testContract, TOKEN_OUT, AMOUNT_OUT_MIN, AMOUNT_IN, token2)
