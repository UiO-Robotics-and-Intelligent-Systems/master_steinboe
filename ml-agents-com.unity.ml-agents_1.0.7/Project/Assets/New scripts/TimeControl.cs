
using UnityEngine;

public class TimeControl : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        Time.timeScale = 1f;
        Time.fixedDeltaTime = Time.fixedDeltaTime*Time.timeScale;
    }


}
