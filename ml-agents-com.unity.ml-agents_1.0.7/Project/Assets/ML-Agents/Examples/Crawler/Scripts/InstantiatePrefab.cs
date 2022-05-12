using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using Unity.MLAgents;
using Unity.MLAgents.SideChannels;
using UnityEngine.SceneManagement;

public class InstantiatePrefab : MonoBehaviour
{
    // instance of this file in the empty gameobject
    private static InstantiatePrefab instance;
    public static InstantiatePrefab Instance
    {
        get { return instance; }
    }
    public bool resetEnvironment = false;

    // Reference to the Prefab. Drag a Prefab into this field in the Inspector.
    public GameObject myPrefab;
    //CameraFollow cameraFollow;
    StringLogSideChannel stringChannel;
    StringLogSideChannelConfig stringChannelConfig;
    String morphologyConfig = "";
    public static int numFixedUpdateAfterReset = 10; // TODO: change, tune or something
    private GameObject fixedPlatform;
    Vector3 OriginalCameraPos = new Vector3(0, 0, 0);
    Quaternion A;
    GameObject head;

    // This script will simply instantiate the Prefab when the game starts.
    public void Awake()
    {
        // 
        if (instance != null && instance != this)
        {

            this.gameObject.SetActive(false);
            Destroy(this.gameObject);
            return;
        }
        else if (instance == null)
        {
            instance = this;
        }
        DontDestroyOnLoad(gameObject);

        // We create the Side Channel
        ///// stringChannel = new StringLogSideChannel();
        if (stringChannel == null)
        {
            stringChannel = new StringLogSideChannel();
            SideChannelsManager.RegisterSideChannel(stringChannel);
            //stringChannelConfig = new StringLogSideChannelConfig();
            //SideChannelsManager.RegisterSideChannel(stringChannelConfig);
        }

        // When a Debug.Log message is created, we send it to the stringChannel
        //Application.logMessageReceived += stringChannel.SendDebugStatementToPython;



        StringLogSideChannel.onReceivedMorph += NewMorphReceived;
        //StringLogSideChannelConfig.onReceivedConfig += ReceivedConfig;
        Academy.Instance.OnEnvironmentReset += EnvironmentReset;
        //SceneManager.sceneLoaded += SceneIsLoaded;


    }



    public void ReceivedConfig(string str)
    {
        //Debug.Log("ReceivedConfig: " + str);
        string[] s = str.Split(',');
        var i = 0;
        Physics.gravity = new Vector3(0, float.Parse(s[i++]), 0);

        //Debug.Log("gravity:" + Physics.gravity);
    }

    public void NewMorphReceived(string str)
    {
        morphologyConfig = str;
    }

    public void EnvironmentReset()
    {
        //Debug.LogError("Reset is called");

        // if reset is called again while executing
        if (resetEnvironment) { return; } //Debug.LogError("Reset was called again");
        resetEnvironment = true;

        // do I need this if-check?
        if (SceneManager.GetActiveScene().isLoaded)
        {   
            //Debug.LogError("Loading scene");
            // resetting the scene (needed for deterministic physics)
            SceneManager.LoadScene(0);
        }


        if (fixedPlatform != null)
        {
            Destroy(fixedPlatform);
            //Debug.LogError("Destroying platform");
        }

        StartCoroutine(InstantiateObject());

    }

    public IEnumerator InstantiateObject()
    {

        //Debug.LogError("Starting coroutine");

        Physics.autoSimulation = false;

        // prøv å endre kroppen her! legg på pupper :)
        //String morphologyConfig = "0,0,-1.0,-1.0,0,0,0,0,1.0,1.0,0,0,0.3,0.5,0.3,0.3,0.5,0.3,0.3,0.5,0.3,0.3,0.5,0.3,0,0,-2.0,-2.0,0,0,0,0,2.0,2.0,0,0,0.3,0.5,0.3,0.3,0.5,0.3,0.3,0.5,0.3,0.3,0.5,0.3";        
        for (int i = 0; i < numFixedUpdateAfterReset; i++)
        { 
            yield return new WaitForFixedUpdate();
        }

        //Debug.LogError("Editing prefab");
        myPrefab.GetComponentInChildren<BodyTransform>().DoThings(morphologyConfig);

        // Instantiate at position (0, 0, 0) and zero rotation.
        //Debug.LogError("Init prefab");
        fixedPlatform = Instantiate(myPrefab, new Vector3(0, 0, 0), Quaternion.identity);

        //for (int i = 0; i < numFixedUpdateAfterReset; i++)
        //{
        yield return new WaitForFixedUpdate();
        //}

        //Debug.LogError("Turning physics back on");
        Physics.autoSimulation = true;

        GameObject head = fixedPlatform.GetComponentInChildren<CrawlerAgent>().head;

        GameObject CameraFoundBySearch = GameObject.Find("Main Camera");
        //Debug.LogError("Setting camera");
        // set camera to original position 
        if (OriginalCameraPos == new Vector3(0, 0, 0))
        {
            OriginalCameraPos = CameraFoundBySearch.transform.position;
        }
        CameraFoundBySearch.transform.position = OriginalCameraPos;

        // set current head to camera-target
        CameraFoundBySearch.GetComponent<CameraFollow>().target = head.transform;


        A = head.transform.rotation;

        //Debug.LogError("Done with resetting");

        resetEnvironment = false;

    }


}