package com.kwkna.codingames.Temperatures;

// https://www.codingame.com/ide/puzzle/temperatures

import java.util.*;
import java.io.*;
import java.math.*;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
class Solution {

    public static void main(String args[]) {

        Scanner in = new Scanner(System.in);

        int n = in.nextInt(); // the number of temperatures to analyse
        int closestTemp = 0;
        if(n>0){
            closestTemp = in.nextInt();
            for (int i = 1; i < n; i++) {
                int t = in.nextInt(); // a temperature expressed as an integer ranging from -273 to 5526
                if(Math.abs(closestTemp) >= Math.abs(t)){
                    if (Math.abs(closestTemp) == Math.abs(t)) {
                        if(t > 0){
                            closestTemp = t;
                        }
                    }
                    else{
                        closestTemp = t;
                    }
                }
            }
        }
        System.out.println(closestTemp);

        // Write an answer using System.out.println()
        // To debug: System.err.println("Debug messages...");

    }
}