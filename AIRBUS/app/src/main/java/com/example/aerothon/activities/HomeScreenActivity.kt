package com.example.aerothon.activities

import android.content.Context
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.fragment.app.FragmentManager
import androidx.recyclerview.widget.RecyclerView
import com.example.aerothon.MainActivity
import com.example.aerothon.R
import com.example.aerothon.adapters.FlightTypeAdapter
import com.example.aerothon.models.FlightTypeModel
import com.example.aerothon.databinding.ActivityHomeScreenBinding
import com.example.aerothon.fragments.FlightDefaultFragment
import com.example.aerothon.models.UserModel
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.ktx.auth
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener
import com.google.firebase.ktx.Firebase

class HomeScreenActivity : AppCompatActivity() {

    private lateinit var binding: ActivityHomeScreenBinding
    private lateinit var recyclerView: RecyclerView
    private lateinit var FlightTypeAdapter: FlightTypeAdapter
    private lateinit var FlightTypeList: ArrayList<FlightTypeModel>
    private lateinit var dialog:AlertDialog
    private lateinit var database: FirebaseDatabase
    private lateinit var auth: FirebaseAuth

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityHomeScreenBinding.inflate(layoutInflater)
        setContentView(binding.root)
        defaultFragmentDisplayed()
        enableBottomNavView()
        enableRecyclerView()
        getNameFromDatabase()

        binding.btnLogout.setOnClickListener {
            logout()
        }

        binding.srit.setOnClickListener {
            startActivity(Intent(this, PersonalityAssessmentActivity::class.java))
        }


//        score = intent.getStringExtra("testScore")!!
//        binding.tvTestScore.text = score

        val sharedPreferences = getSharedPreferences("MyPrefs", Context.MODE_PRIVATE)
        val score = sharedPreferences.getString("testScore","")
//        binding.tvTestScore.text = score
        if(score!!.toInt()>=29.5){
            binding.tvTestScore.text = score!! +" good"
        }
        else{
            binding.tvTestScore.text = score!!+ " bad"
        }
    }


    private fun enableRecyclerView(){
        recyclerView = binding.recyclerView
        FlightTypeList = ArrayList()
        FlightTypeList.add(FlightTypeModel("Flights", R.drawable.Flights))
        FlightTypeList.add(FlightTypeModel("Competitions", R.drawable.comp))
        FlightTypeList.add(FlightTypeModel("Mentorship", R.drawable.mentorship))
        FlightTypeList.add(FlightTypeModel("Field", R.drawable.field))
        FlightTypeAdapter = FlightTypeAdapter(FlightTypeList,this)
        recyclerView.adapter = FlightTypeAdapter

    }

    private fun enableBottomNavView(){
        val bottomNavigationView = binding.bottomNavigation
        bottomNavigationView.setSelectedItemId(R.id.homeScreen)
        bottomNavigationView.setOnNavigationItemSelectedListener { item ->
            when (item.itemId) {
                R.id.statusScreen -> {
                    startActivity(Intent(applicationContext, StatusScreenActivity::class.java))
                    finish()
                    overridePendingTransition(0, 0)
                    true
                }
                R.id.homeScreen -> true
                R.id.supportScreen -> {
                    startActivity(Intent(applicationContext, SupportScreenActivity::class.java))
                    finish()
                    overridePendingTransition(0, 0)
                    true
                }
                R.id.notificationsScreen -> {
                    startActivity(Intent(applicationContext, NotificationsScreenActivity::class.java))
                    finish()
                    overridePendingTransition(0, 0)
                    true
                }
                else -> false
            }
        }
    }

    private fun getNameFromDatabase(){
        database = FirebaseDatabase.getInstance()
        dialogBox("Retrieving Data from FB Realtime DB","Please Wait ...")
        database.reference.child("users")
            .addValueEventListener(object : ValueEventListener {
                override fun onDataChange(snapshot: DataSnapshot) {
                    for(snapshot1 in snapshot.children){
                        val user = snapshot1.getValue(UserModel::class.java)
                        if(user!!.uid == FirebaseAuth.getInstance().uid){
                            binding.tvUsername.text = user.name
                            dialog.dismiss()
                            break
                        }
                    }

                }
                override fun onCancelled(error: DatabaseError) {
                    dialog.dismiss()
                }
            })
    }


    private fun dialogBox(title:String,message:String){
        val builder = AlertDialog.Builder(this)
        builder.setMessage(message)
        builder.setTitle(title)
        builder.setCancelable(false)
        dialog = builder.create()
        dialog.show()
    }

    private fun logout(){
        auth = Firebase.auth
        Toast.makeText(applicationContext,"Logged out", Toast.LENGTH_SHORT).show()
        auth.signOut()
        startActivity(Intent(this, MainActivity::class.java))
        finish()
    }

    private fun defaultFragmentDisplayed(){
        val fragmentContainer = binding.fragmentContainerView
        // Check if the fragment is already added to avoid adding it multiple times
        val defaultFragment = FlightDefaultFragment()
        val fragmentManager = supportFragmentManager
        fragmentManager.popBackStackImmediate(null, FragmentManager.POP_BACK_STACK_INCLUSIVE)
        val transaction = fragmentManager.beginTransaction()
        transaction.replace(fragmentContainer.id, defaultFragment)
        transaction.commit()
    }


}