using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using Unity.MLAgents;
using Unity.MLAgents.SideChannels;
using UnityEngine.SceneManagement;

public class BodyTransform : MonoBehaviour
{
    [Header("Array of legs")]
    [SerializeField] GameObject[] legs;

    [SerializeField] GameObject head;
    StringLogSideChannel stringChannel;
    String morphologyConfig="";
    int density=1000/64;
    private Scene scene;
    // public void Awake()
    // {
    //     // We create the Side Channel
    //     ///// stringChannel = new StringLogSideChannel();
    //     if (stringChannel == null){
    //         stringChannel = StringLogSideChannel.Instance;
    //         SideChannelsManager.RegisterSideChannel(stringChannel);
    //     }
// 
    //     // When a Debug.Log message is created, we send it to the stringChannel
    //     // TODO?: Application.logMessageReceived += stringChannel.SendDebugStatementToPython;
    //     
    //     // The channel must be registered with the SideChannelsManager class
    //     //SideChannelsManager.RegisterSideChannel(stringChannel);
// 
    //     StringLogSideChannel.onReceivedMorph += NewMorphReceived;
    //     //Academy.Instance.OnEnvironmentReset += EnvironmentReset;
    //     //SceneManager.sceneLoaded += SceneIsLoaded;
// 
    // }
    public void DoThings(String str)
    {
        morphologyConfig =str;
        if (morphologyConfig=="")
        {
            ResetMorphology();
        }
        else 
        {
            SetMorphology(morphologyConfig);
        }
        //legs[0].transform.localPosition = new Vector3(0,0,4);


    }

    // kall på sendString, så kjør reset for å starte den nye kroppen!
    

    public void SetMorphologyEnumerator()
    {

        // setting new morphology
        //Debug.Log("setting morphology");
        if (morphologyConfig=="") 
        {
            ResetMorphology();
        }
        else
        {
            SetMorphology(morphologyConfig);
        }
        //Debug.Log("morphology is set");
        morphologyConfig = "";

        //Debug.Log("setMorphologyEnumerator is done");
    }




    public void SetMorphology(String str)
    {        
        //Debug.Log("Setting morphology"+str);
        List<Vector3> legLen = new List<Vector3>();
        List<Vector3> pos = new List<Vector3>();

        //Debug.Log("str:"+str);

        //str = str.Replace("(", "").Replace(")"," ");//Replace "(" and ")" in the string with ""
        string[] s = str.Split(',');
        // the ArgumentOutOfRangeException occures with all idexes above 0 
        // Debug.Log(s.Length);
        // change the data here
        // upper
        var i = 0; // går til: 3*4*4-1=47
        pos.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++]))); // legg0Upper
        pos.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++])));// legg1Upper
        pos.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++])));// legg2Upper
        pos.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++]))); // legg3Upper

        legLen.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++]))); // legg0Upper
        legLen.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++]))); // legg1Upper
        legLen.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++]))); // legg2Upper 
        legLen.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++]))); // legg3Upper
        
        // lower
        pos.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++]))); // legg0Lower
        pos.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++]))); // legg1Lower
        pos.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++])));// legg2Lower
        pos.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++])));// legg3Lower

        legLen.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++]))); // legg0Lower
        legLen.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++]))); // legg1Lower
        legLen.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++]))); // legg2Lower
        legLen.Add(new Vector3(float.Parse(s[i++]), float.Parse(s[i++]), float.Parse(s[i++]))); // legg3Lower
        /////
        ChangeBody(legLen, pos);
        
    }

    public void ResetMorphology() {
        //Debug.Log("ResetMorphology");
        List<Vector3> legLen = new List<Vector3>();
        List<Vector3> pos = new List<Vector3>();

        // upper
        pos.Add(new Vector3(0.0f, 0.0f, -1.0f)); // legg0Upper
        pos.Add(new Vector3(-1.0f, 0.0f, 0.0f)); // legg1Upper
        pos.Add(new Vector3(0.0f, 0.0f, 1.0f)); // legg2Upper
        pos.Add(new Vector3(1.0f, 0.0f, 0.0f)); // legg3Upper

        legLen.Add(new Vector3(0.3f, 0.5f, 0.3f)); // legg0Upper
        legLen.Add(new Vector3(0.3f, 0.5f, 0.3f)); // legg1Upper
        legLen.Add(new Vector3(0.3f, 0.5f, 0.3f)); // legg2Upper 
        legLen.Add(new Vector3(0.3f, 0.5f, 0.3f)); // legg3Upper
        
        // lower
        pos.Add(new Vector3(0.0f, 0.0f, -2.5f)); // legg0Lower
        pos.Add(new Vector3(-2.5f, 0.0f, 0.0f)); // legg1Lower
        pos.Add(new Vector3(0.0f, 0.0f, 2.5f)); // legg2Lower
        pos.Add(new Vector3(2.5f, 0.0f, 0.0f)); // legg3Lower

        legLen.Add(new Vector3(0.3f, 1.0f, 0.3f)); // legg0Lower
        legLen.Add(new Vector3(0.3f, 1.0f, 0.3f)); // legg1Lower
        legLen.Add(new Vector3(0.3f, 1.0f, 0.3f)); // legg2Lower
        legLen.Add(new Vector3(0.3f, 1.0f, 0.3f)); // legg3Lower
        /////
        ChangeBody(legLen, pos);
    }

    public void ResetMorphology2() {
        //Debug.Log("ResetMorphology2");
        List<Vector3> legLen = new List<Vector3>();
        List<Vector3> pos = new List<Vector3>();

        // upper
        pos.Add(new Vector3(0.0f, 0.0f, -1.0f)); // legg0Upper
        pos.Add(new Vector3(-1.0f, 0.0f, 0.0f)); // legg1Upper
        pos.Add(new Vector3(0.0f, 0.0f, 1.0f)); // legg2Upper
        pos.Add(new Vector3(1.0f, 0.0f, 0.0f)); // legg3Upper

        legLen.Add(new Vector3(0.3f, 0.5f, 0.3f)); // legg0Upper
        legLen.Add(new Vector3(0.3f, 0.5f, 0.3f)); // legg1Upper
        legLen.Add(new Vector3(0.3f, 0.5f, 0.3f)); // legg2Upper 
        legLen.Add(new Vector3(0.3f, 0.5f, 0.3f)); // legg3Upper
        
        // lower
        pos.Add(new Vector3(0.0f, 0.0f, -2.5f)); // legg0Lower
        pos.Add(new Vector3(-2.5f, 0.0f, 0.0f)); // legg1Lower
        pos.Add(new Vector3(0.0f, 0.0f, 2.5f)); // legg2Lower
        pos.Add(new Vector3(2.5f, 0.0f, 0.0f)); // legg3Lower

        legLen.Add(new Vector3(0.3f, 1.0f, 0.3f)); // legg0Lower
        legLen.Add(new Vector3(0.3f, 1.0f, 0.3f)); // legg1Lower
        legLen.Add(new Vector3(0.3f, 1.0f, 0.3f)); // legg2Lower
        legLen.Add(new Vector3(0.3f, 1.0f, 0.3f)); // legg3Lower
        /////
        ChangeBody(legLen, pos);
    }

    public void ChangeBody(List<Vector3> lengths, List<Vector3> positions)
    {
        //if (Application.isPlaying) {
        //    for (int i=0; i<8;i++)
        //    {
        //        legs[i].SetActive(false);
        //    }
        //}
        //// 
        for (int i = 0; i < 8; i++)
        {
            GameObject leg = legs[i];
            Vector3 length = lengths[i];
            Vector3 pos = positions[i];

            SetLegPosAndLength(leg, length, pos);
            // Debug.Log("i:"+i+"localScale:"+leg.transform.localScale);
            // Debug.Log("i:"+i+"localPosition:"+leg.transform.localPosition);

        }

        //if (Application.isPlaying) {
        //    for (int i=0; i<8;i++) 
        //    {
        //        legs[i].SetActive(true);
        //    }
        //}
    }

    private void SetLegPosAndLength(GameObject leg, Vector3 length, Vector3 pos)
    {
        leg.transform.localScale = length;
        leg.transform.localPosition = pos;
        leg.GetComponent<Rigidbody>().mass=density*leg.transform.localScale.y;
        //leg.GetComponent<Rigidbody>().mass=density*leg.transform.localScale.x*leg.transform.localScale.y*leg.transform.localScale.z;
    }


}
