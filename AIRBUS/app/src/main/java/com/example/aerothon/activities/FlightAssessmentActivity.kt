package com.example.aerothon.activities

import android.content.Context
import android.content.Intent
import android.graphics.Color
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.fragment.app.FragmentManager
import androidx.recyclerview.widget.RecyclerView
import com.example.aerothon.adapters.FLightAssessmentAdapter
import com.example.aerothon.models.PersonalityAssessmentQuestionModel
import com.example.aerothon.databinding.ActivityPersonalityAssessmentBinding
import com.example.aerothon.fragments.AssessmentDefaultFragment
import com.google.android.material.snackbar.BaseTransientBottomBar
import com.google.android.material.snackbar.Snackbar

class FlightAssessmentActivity : AppCompatActivity() {

    private lateinit var binding: ActivityPersonalityAssessmentBinding
    private lateinit var recyclerView: RecyclerView
    private lateinit var questionsList: ArrayList<PersonalityAssessmentQuestionModel>
    private lateinit var questionsAdapter: FLightAssessmentAdapter
    lateinit var score:String

    val flightConditionsQuestions = arrayOf(
        arrayOf(
            "What is the current weather at the departure airport?",
            "Clear skies",
            "Partly cloudy",
            "Overcast",
            "Stormy",
            "null"
        ),
        arrayOf(
            "What is the current weather at the arrival airport?",
            "Clear skies",
            "Partly cloudy",
            "Overcast",
            "Stormy",
            "null"
        ),
        arrayOf(
            "What is the current wind speed at the departure airport?",
            "Calm (0-5 mph)",
            "Moderate (6-15 mph)",
            "Strong (16-30 mph)",
            "Severe (>30 mph)",
            "null"
        ),
        arrayOf(
            "What is the current wind speed at the arrival airport?",
            "Calm (0-5 mph)",
            "Moderate (6-15 mph)",
            "Strong (16-30 mph)",
            "Severe (>30 mph)",
            "null"
        ),
        arrayOf(
            "Are there any weather advisories or warnings for the flight path?",
            "No advisories or warnings",
            "Minor advisories",
            "Moderate warnings",
            "Severe warnings",
            "null"
        ),
        arrayOf(
            "Is the aircraft fully fueled and ready for departure?",
            "Yes, fully fueled",
            "Partially fueled",
            "Not fueled",
            "Unknown",
            "null"
        ),
        arrayOf(
            "Is the flight crew fully staffed and ready for the flight?",
            "Yes, fully staffed",
            "Partially staffed",
            "Crew missing",
            "Unknown",
            "null"
        ),
        arrayOf(
            "Are all necessary pre-flight checks completed?",
            "Yes, all checks completed",
            "Some checks completed",
            "No checks completed",
            "Unknown",
            "null"
        ),
        arrayOf(
            "Are there any mechanical issues with the aircraft?",
            "No issues",
            "Minor issues",
            "Major issues",
            "Unknown",
            "null"
        ),
        arrayOf(
            "Are all passengers accounted for and seated?",
            "Yes, all accounted for",
            "Some missing",
            "Many missing",
            "Unknown",
            "null"
        ),
        arrayOf(
            "Are all passenger luggage loaded and secured?",
            "Yes, all luggage loaded",
            "Some luggage missing",
            "Many luggage missing",
            "Unknown",
            "null"
        )
    )


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityPersonalityAssessmentBinding.inflate(layoutInflater)
        setContentView(binding.root)

        enableRecyclerView()
        defaultFragmentDisplayed()
        nextBtn()
    }


    private fun enableRecyclerView(){
        recyclerView = binding.recyclerView
        questionsList = ArrayList()
        questionsList.add(PersonalityAssessmentQuestionModel("1"))
        questionsList.add(PersonalityAssessmentQuestionModel("2"))
        questionsList.add(PersonalityAssessmentQuestionModel("3"))
        questionsList.add(PersonalityAssessmentQuestionModel("4"))
        questionsList.add(PersonalityAssessmentQuestionModel("5"))
        questionsList.add(PersonalityAssessmentQuestionModel("6"))
        questionsList.add(PersonalityAssessmentQuestionModel("7"))
        questionsList.add(PersonalityAssessmentQuestionModel("8"))
        questionsList.add(PersonalityAssessmentQuestionModel("9"))
        questionsList.add(PersonalityAssessmentQuestionModel("10"))
        questionsList.add(PersonalityAssessmentQuestionModel("11"))


        questionsAdapter = FLightAssessmentAdapter(questionsList,this)
        recyclerView.adapter = questionsAdapter

    }

    private fun nextBtn(){

        binding.btnNext.setOnClickListener {
            var flag:Boolean = false
            for(i in 0..9){
                if(questions[i][5]=="null"){
                    flag = true
                    break
                }
            }
            if(flag){
//                Toast.makeText(this,"incomplete questions",Toast.LENGTH_SHORT).show()
                createSnackBar(binding.root, "incomplete questions","Try Again")
                binding.score.text = calculateAssessmentScore().toString()
            }
            else{
                Toast.makeText(this,"completed questions",Toast.LENGTH_SHORT).show()
                score= calculateAssessmentScore().toString()

                val sharedPreferences = getSharedPreferences("MyPrefs", Context.MODE_PRIVATE)
                val editor = sharedPreferences.edit()
                editor.putString("testScore", score)
                editor.apply()

                val intent = Intent(this,HomeScreenActivity::class.java)
//                intent.putExtra("testScore",score)
                startActivity(intent)


            }
        }

    }


    private fun calculateAssessmentScore():Int{
        var ans:Int= 0
        for(i in 0..questions.size-1){
            val x = questions[i][5]
            if(x=="0"){
                ans+=5
            }
            else if(x=="1"){
                ans+=3
            }
            else if(x=="2"){
                ans+=1
            }
            else if(x=="3"){
                ans+=0
            }
            else{
                ans+=0
            }
        }
        return ans
    }



    private fun createSnackBar(view: View, text: String, actionText:String){
        Snackbar.make(view,text, Snackbar.LENGTH_INDEFINITE)
            .setAnimationMode(BaseTransientBottomBar.ANIMATION_MODE_SLIDE)
            .setBackgroundTint(Color.parseColor("#FF9494"))
            .setTextColor(Color.parseColor("#EE4B28"))
            .setActionTextColor(Color.parseColor("#000000"))
            .setAction(actionText){
//                Toast.makeText(this,"snackbar button pressed",Toast.LENGTH_SHORT).show()
            }
            .show()
    }

    private fun defaultFragmentDisplayed(){
        val fragmentContainer = binding.fragmentContainerView
        // Check if the fragment is already added to avoid adding it multiple times
        val defaultFragment = AssessmentDefaultFragment()
        val fragmentManager = supportFragmentManager
        fragmentManager.popBackStackImmediate(null, FragmentManager.POP_BACK_STACK_INCLUSIVE)
        val transaction = fragmentManager.beginTransaction()
        transaction.replace(fragmentContainer.id, defaultFragment)
        transaction.commit()

    }




}