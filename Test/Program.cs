using System;
using System.Linq;
using System.Collections.Generic;

class MainApp
{
    public static void Main()
    {
        int inputNum = int.Parse(Console.ReadLine());
        int min = -1;
        if (inputNum % 3 == 0) min = inputNum / 3;
        for (int i = 0; i < inputNum / 3; i++)
        {
            var buffer = inputNum - i * 3;
            if (buffer % 5 == 0)
            {
                if (min == -1)
                {
                    min = buffer / 5 + i;
                }
                else if (min > buffer / 5 + i)
                {
                    min = buffer / 5 + i;
                }
            }
        }
        Console.WriteLine(min);
    }
}