from scripts.deploy_and_swap import deploy
import pytest
from scripts.helpful_scripts import (
    get_account,
    get_contract_address,
    FORKED_LOCAL_ENVIRONMENTS,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from brownie import network, exceptions


def test_set_addresses():
    # Arrange
    print(network.show_active())
    if network.show_active() not in FORKED_LOCAL_ENVIRONMENTS:
        pytest.skip("Only for local testing!")

    account = get_account()
    non_owner = get_account(index=1)

    testContract = deploy()
    # act
    routerAddress = get_contract_address("uniswap_router_v2")
    wethAddress = get_contract_address("weth")
    # daiAddress = get_contract_address("dai")

    testContract.setRouter(routerAddress, {"from": account})
    assert routerAddress == testContract.UNISWAP_V2_ROUTER()

    testContract.setWETH(wethAddress, {"from": account})
    assert wethAddress == testContract.WETH()

    with pytest.raises(exceptions.VirtualMachineError):
        testContract.setRouter(routerAddress, {"from": non_owner}).wait(1)

    with pytest.raises(exceptions.VirtualMachineError):
        testContract.setWETH(wethAddress, {"from": non_owner}).wait(1)
