

function csrf_token() {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'))
            }
        }
    });
}
// add cardiologist btn onClick
function addCardiologist_onclick() {
    var name = document.getElementById("cardiologistName").value;
    var experience = document.getElementById("cardiologistExperience").value;
    var genderFemale = document.getElementById("cardiologistGenderFemale").checked;
    var specialization = document.getElementById("cardiologistSpecialization").value;
    var phonenumber = document.getElementById("cardiologistPhonenumber").value;
    var briefInfo = document.getElementById("cardiologistBriefInfo").value;
    var age = document.getElementById("cardiologistAge").value;
    var gender = "m";
    if(genderFemale ==true){
        gender = "f"
    }
    csrf_token();
    $.ajax({
        type: "POST",
        url: "addCardiologist/",
        data: {
            "name":name,
            "experience":experience,
            "gender":gender,
            "specialization":specialization,
            "phonenumber":phonenumber,
            "age":age,
            "briefInfo":briefInfo
        },
        success:function(response){
            if (response =="Successfully created"){
                alert(response);
            window.location.replace("Affiliated-Cardiologists");
            }else{
                alert(response);
            }
        }
    });
}

// add appointment
function add_appointment_onclick(){
    var patientName = document.getElementById("patientName").value;
    var dueDate = document.getElementById("dueDate").value;
    var dueTime = document.getElementById("dueTime").value;
    var cardiologistName = document.getElementById("cardiologistNameAppointmentForm").value;
    var genderFemale = document.getElementById("patientGenderFemale").checked;
    var patientPhonenumber = document.getElementById("patientPhonenumber").value;
    var patientInsurance = document.getElementById("patientInsurance").value;
    var patientMedicalHistory = document.getElementById("patientMedicalHistory").value;
    var patientAge = document.getElementById("patientAge").value;
    var gender = "m";
    if(genderFemale ==true){
        gender = "f"
    }
    csrf_token();
    $.ajax({
        type: "POST",
        url: "addAppointment/",
        data: {
            "name":patientName,
            "age":patientAge,
            "dueDate":dueDate,
            "dueTime":dueTime,
            "phonenumber":patientPhonenumber,
            "medicalHistory":patientMedicalHistory,
            "cardiologistName":cardiologistName,
            "gender":gender,
            "patientInsurance":patientInsurance
        },
        success:function(response){
            if (response =="Successfully created"){
                alert(response);
            window.location.replace("Appointments");
            }else{
                alert(response);
            }
        }
    });
}
function add_test_onclick(){
    var name = document.getElementById("testName").value;
    var patientName = document.getElementById("patientNameTestForm").value;
    var cardiologistName = document.getElementById("cardiologistNameTestForm").value;
    var cost = document.getElementById("testCost").value;
    var status = document.getElementById("testStatus").value;
    
    csrf_token();
    $.ajax({
        type: "POST",
        url: "addTest/",
        data: {
            "name":name,
            "patientName":patientName,
            "cardiologistName":cardiologistName,
            "cost":cost,
            "status":status,
            
        },
        success:function(response){
            if (response =="Successfully created"){
                alert(response);
            window.location.replace("Tests");
            }else{
                alert(response);
            }
        }
    });
}

// add nurse
function add_nurse_onclick(){
    var name = document.getElementById("nurseName").value;
    var phonenumber = document.getElementById("nursePhonenumber").value;
    var patients = []
    var selectedPatients = document.getElementsByClassName("nursePatient");
    for(var element of selectedPatients){
        if(element.checked){
            patients.push(element.value)
        }
    }
    
    var age = document.getElementById("nurseAge").value;
    
    
    csrf_token();
    $.ajax({
        type: "POST",
        url: "addNurse/",
        data: {
            "name":name,
            "phonenumber":phonenumber,
            "patients":"["+patients+"]",
            "age":age,
   
        },
        success:function(response){
            if (response =="Successfully created"){
                alert(response);
            window.location.replace("Nurses");
            }else{
                alert(response);
            }
        }
    });
}