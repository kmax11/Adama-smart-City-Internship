// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Contract {
    enum Foods { Apple, Banana, Pizza, Bagel }

    Foods public food1 = Foods.Apple;
    Foods public food2 = Foods.Banana;
    Foods public food3 = Foods.Pizza;
    Foods public food4 = Foods.Bagel;
}