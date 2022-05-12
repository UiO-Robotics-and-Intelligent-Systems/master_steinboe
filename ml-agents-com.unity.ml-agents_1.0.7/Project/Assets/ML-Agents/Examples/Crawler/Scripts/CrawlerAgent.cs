using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgentsExamples;
using Unity.MLAgents.Sensors;
using System.Collections.Generic;

[RequireComponent(typeof(JointDriveController))] // Required to set joint forces
public class CrawlerAgent : Agent
{

    [Header("Head (gameobject)")]
    [Space(10)]
    public GameObject head;

    [Header("Legs (transform)")]
    [Space(10)]
    public Transform leg0Upper;
    public Transform leg0Lower;
    public Transform leg1Upper;
    public Transform leg1Lower;
    public Transform leg2Upper;
    public Transform leg2Lower;
    public Transform leg3Upper;
    public Transform leg3Lower;

    [Header("Joint Settings")] [Space(10)] JointDriveController m_JdController;

    Vector3 initPos;
    Quaternion originalRotation;
    bool evaluate = false;

    private static ILogger logger = Debug.unityLogger;
    public override void Initialize()
    {
        /// ###################
        logger.logEnabled = Debug.isDebugBuild;

        m_JdController = GetComponent<JointDriveController>();
        initPos = head.transform.position;

        //Setup each body part
        m_JdController.SetupBodyPart(head.transform);
        m_JdController.SetupBodyPart(leg0Upper);
        m_JdController.SetupBodyPart(leg0Lower);
        m_JdController.SetupBodyPart(leg1Upper);
        m_JdController.SetupBodyPart(leg1Lower);
        m_JdController.SetupBodyPart(leg2Upper);
        m_JdController.SetupBodyPart(leg2Lower);
        m_JdController.SetupBodyPart(leg3Upper);
        m_JdController.SetupBodyPart(leg3Lower);

        originalRotation = head.transform.rotation;
    }


    public override void CollectObservations(VectorSensor sensor)
    {   //  "Called every step that the Agent requests a decision" ofte nok? jaaa det tror jeg :)      
        // todo: implement stability measure? remove. Use rewardStability instead :) or?
        if (evaluate)
        {
            // call both rewardFunctions
            //if (sensor != null)
            //{
                
                RewardDistancedTraveled();
                RewardStability(sensor);
            //}
        }
        else {
            for (int i=0; i<6; i++) {
                sensor.AddObservation(0);
            }   
        }
    }




    /// <summary>
    /// todo
    /// </summary>
    void RewardDistancedTraveled()
    {
        SetReward((head.transform.position-initPos).x);
    }

    /// <summary>
    /// todo
    /// </summary>
    void RewardStability(VectorSensor sensor)
    {
        // calculating orientation:

        var currentRotation = head.transform.rotation;
        var diffRotation = currentRotation * Quaternion.Inverse(originalRotation);

        var diffEuler = new Vector3();

        for (int i = 0; i < 3; i++)
        {
            if (diffRotation.eulerAngles[i] > 180)
            {
                diffEuler[i] = diffRotation.eulerAngles[i] - 360;
            }
            else
            {
                diffEuler[i] = diffRotation.eulerAngles[i];


            }
        }

        sensor.AddObservation(diffEuler); // the difference in orientation from the original orientation
        // x, y, z. Can choose to not look at z (will change with different legsizes and while walking forward)
        // x - from front
        // y - from top
        // z - from side (left of walking direction)

        //sensor.AddObservation(1);

        // The velocity vector of the rigidbody (could be used for linear acceleration):
        var rigidBody = head.GetComponent<Rigidbody>();
        sensor.AddObservation(rigidBody.velocity); // yes
        // can avoid z-axis. Should do so yes
    }





    /// <summary>
    /// todo
    /// </summary>
    public override void OnActionReceived(float[] vectorAction)
    {
        // vectorAction: [-1,1]
        if (evaluate == false && vectorAction[0] == 1) // happens only once. The first time index 0 is 1
        {
            // happens only ones pr evaluations
            initPos = head.transform.position;
            evaluate = true;
        }

        // The dictionary with all the body parts in it are in the jdController
        var bpDict = m_JdController.bodyPartsDict;

        var i = -1;
        // Pick a new target joint rotation 
        bpDict[leg0Upper].SetJointTargetRotation(vectorAction[++i], vectorAction[++i], 0);
        bpDict[leg1Upper].SetJointTargetRotation(vectorAction[++i], vectorAction[++i], 0);
        bpDict[leg2Upper].SetJointTargetRotation(vectorAction[++i], vectorAction[++i], 0);
        bpDict[leg3Upper].SetJointTargetRotation(vectorAction[++i], vectorAction[++i], 0);
        bpDict[leg0Lower].SetJointTargetRotation(vectorAction[++i], 0, 0);
        bpDict[leg1Lower].SetJointTargetRotation(vectorAction[++i], 0, 0);
        bpDict[leg2Lower].SetJointTargetRotation(vectorAction[++i], 0, 0);
        bpDict[leg3Lower].SetJointTargetRotation(vectorAction[++i], 0, 0);

        // Update joint strength
        bpDict[leg0Upper].SetJointStrength(vectorAction[++i]);
        bpDict[leg0Lower].SetJointStrength(vectorAction[++i]);
        bpDict[leg1Upper].SetJointStrength(vectorAction[++i]);
        bpDict[leg1Lower].SetJointStrength(vectorAction[++i]);
        bpDict[leg2Upper].SetJointStrength(vectorAction[++i]);
        bpDict[leg2Lower].SetJointStrength(vectorAction[++i]);
        bpDict[leg3Upper].SetJointStrength(vectorAction[++i]);
        bpDict[leg3Lower].SetJointStrength(vectorAction[++i]);
    }














    // not in use anymore:
    void FixedUpdate() // what is this, and why is it not Update?
    {
        // Set reward for this step according to mixture of the following elements.
       
    }
    
}
