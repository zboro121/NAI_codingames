package com.kwkna.codingames.horseRacingDuals;

// https://www.codingame.com/ide/puzzle/horse-racing-duals

import java.util.*;
import java.io.*;
import java.math.*;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
class Solution {

    public static void main(String args[]) {
        List<Integer> horses = new ArrayList<>();
        int matchedStr = -1;
        Scanner in = new Scanner(System.in);
        int N = in.nextInt();

        for (int i = 0; i < N; i++) {
            int pi = in.nextInt();
            horses.add(pi);
        }

        Collections.sort(horses);
        int prevHorse = horses.get(0);
        for (int i = 1; i < N; i++) {
            int horse = horses.get(i);
            int str = horse - prevHorse;
            if(matchedStr == -1 || str<matchedStr){
                matchedStr = str;
            }
            prevHorse = horse;

        }

        // Write an answer using System.out.println()
        // To debug: System.err.println("Debug messages...");

        System.out.println(matchedStr);
    }
}
