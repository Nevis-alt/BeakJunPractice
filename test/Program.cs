using System;
using System.Collections.Generic;

class Program
{
    static readonly string[] CHO = { "ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ" };
    static readonly string[] JUNG = { "ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ" };
    static readonly string[] JONG = { "","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ" };

    static List<string> DecomposeHangul(string s)
    {
        List<string> result = new List<string>();
        foreach (char ch in s)
        {
            int code = ch - 0xAC00;
            if (code >= 0 && code < 11172)
            {
                int cho = code / 588;
                int jung = (code % 588) / 28;
                int jong = code % 28;

                result.Add(CHO[cho]);
                result.Add(JUNG[jung]);
                if (jong != 0)
                    result.Add(JONG[jong]);
            }
            else
            {
                // 비한글 문자 그대로 추가
                result.Add(ch.ToString());
            }
        }
        return result;
    }

    static string CompareKoreanDynamic(string correct, string typed)
    {
        if (correct == typed)
            return "correct";

        var correctDecomp = DecomposeHangul(correct);
        var typedDecomp = DecomposeHangul(typed);

        int len = typedDecomp.Count;
        if (len <= correctDecomp.Count)
        {
            bool match = true;
            for (int i = 0; i < len; i++)
            {
                if (correctDecomp[i] != typedDecomp[i])
                {
                    match = false;
                    break;
                }
            }
            if (match)
                return "progress";
        }
        return "wrong";
    }

    static void Main()
    {
        var tests = new (string correct, string typed)[]
        {
            ("삽", "ㅅ"),
            ("삽", "사"),
            ("삽", "삽"),
            ("삽", "살"),
            ("삽", "샤"),
        };

        foreach (var (correct, typed) in tests)
        {
            string result = CompareKoreanDynamic(correct, typed);
            Console.WriteLine($"입력: '{typed}' → {result}");
        }
        Console.WriteLine("마ㄴㅇㄹ".Length);
    }
}
