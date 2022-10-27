// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0;

//import "./interfaces/IERC20.sol";
//mport ".././interfaces/Uniswap2.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@uniswap/contracts/interfaces/IWETH.sol";
import "@uniswap/contracts/interfaces/IUniswapV2Router02.sol";


contract UniswapV2Swap is Ownable {
    //address private constant UNISWAP_V2_ROUTER = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    //address private constant WETH = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;

    //address private constant UNISWAP_V2_ROUTER = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    //address private constant WETH = 0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6;

    address public UNISWAP_V2_ROUTER;
    address public WETH;

    function swap(address _tokenOut, uint256 _amountOutMin, address _to) external payable {
        
        IWETH(WETH).deposit{value: msg.value}();
        
        address [] memory path;
        path = new address[](2);
        //path[0] = _tokenIn;
        path[0] = WETH;
        path[1] = _tokenOut;

        IERC20(WETH).approve(UNISWAP_V2_ROUTER,msg.value);
        IUniswapV2Router02(UNISWAP_V2_ROUTER).swapExactTokensForTokensSupportingFeeOnTransferTokens( msg.value, _amountOutMin, path, _to, block.timestamp);
    }

    function setRouter(address _address) public onlyOwner {
        UNISWAP_V2_ROUTER = _address;
    }

    function setWETH(address _address) public onlyOwner {
        WETH = _address;
    }
}
