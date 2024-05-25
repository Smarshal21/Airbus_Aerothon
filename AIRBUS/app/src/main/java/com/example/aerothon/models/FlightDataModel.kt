package com.example.aerothon.models

data class FlightDataModel(
    val flightNumber: String? = null,
    val departureAirport: String? = null,
    val arrivalAirport: String? = null,
    val departureTime: String? = null,
    val arrivalTime: String? = null,
    val aircraftType: String? = null,
    val aircraftID: String? = null,
    val currentWeatherDeparture: String? = null,
    val currentWeatherArrival: String? = null,
    val windSpeedDeparture: String? = null,
    val windSpeedArrival: String? = null,
    val weatherAdvisories: String? = null,
    val fuelStatus: String? = null,
    val crewStatus: String? = null,
    val preFlightChecks: String? = null,
    val mechanicalIssues: String? = null,
    val passengerCount: String? = null,
    val passengerStatus: String? = null,
    val luggageStatus: String? = null,
    val additionalInfo: String? = null,
    val mlOutput: String? = null
)
