using System;
using System.Collections;
using System.Collections.Generic;
//using UnityEngine;
//string slist = "2.32113,343.2342,5.3242";
//string s1 = "1.7877844545";
//float f1 = float.Parse(slist);
//
//Console.Write(f1);

        



string str = "0.45, -145, 63.5";
//data.Split(',');
//Console.Write(data.GetType());

str = str.Replace("(", "").Replace(")"," ");//Replace "(" and ")" in the string with ""
string[] s = str.Split(',');
Vector3 vector= new Vector3(float.Parse(s[0]), float.Parse(s[1]), float.Parse(s[2]));

Console.Write(vector);