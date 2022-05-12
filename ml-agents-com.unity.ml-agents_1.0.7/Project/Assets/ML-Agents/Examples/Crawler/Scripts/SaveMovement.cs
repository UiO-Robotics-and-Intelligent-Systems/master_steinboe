using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Threading.Tasks;

public class SaveMovement : MonoBehaviour
{
    [Header("Gameobjects")]
    [SerializeField] GameObject[] legs;

    [SerializeField] GameObject head;

    // Start is called before the first frame update
    void Start()
    {

    }

    //void FixedUpdate()
    //{
    //    Debug.Log("head");
    //    Debug.Log(head.transform.rotation);
    //    Debug.Log(head.transform.position); 
    //    Debug.Log(head.transform.localScale);  
    //    ExampleAsync();
    //    // same for all legs
    //}
//
    //public static async Task ExampleAsync()
    //{
    //    using StreamWriter file = new("WriteLines2.txt", append: true);
    //    await file.WriteLineAsync("Fourth line");
    //}
}
