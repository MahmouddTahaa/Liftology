// document.getElementById("predictForm").addEventListener("submit", async (e) => {
//   e.preventDefault();

//   if (
//     validateInput(
//       document.getElementById("weight"),
//       /^(30|[3-9][0-9]|1[0-9]{2}|2[0-4][0-9]|250)$/
//     ) &&
//     validateInput(
//       document.getElementById("height"),
//       /^(5[0-9]|[6-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/
//     ) &&
//     validateInput(
//       document.getElementById("bmi"),
//       /^(1[0-9]|2[0-9]|3[0-9]|4[0-9]|50)(\.\d{1,2})?$/
//     ) &&
//     validateInput(
//       document.getElementById("bodyFat"),
//       /^(100(?:\.0{1,2})?|[0-9]{1,2}(?:\.[0-9]{1,2})?)$/
//     ) &&
//     validateInput(
//       document.getElementById("age"),
//       /^(?:[1-9]?[0-9]|1[01][0-9]|120)$/
//     ) &&
//     validateInput(document.getElementById("gender"), /(male|female)/)
//   ) {
//     const payload = {
//       weight: parseFloat(document.getElementById("weight").value),
//       height: parseFloat(document.getElementById("height").value / 100),
//       bmi: parseFloat(document.getElementById("bmi").value),
//       body_fat_percentage: parseFloat(document.getElementById("bodyFat").value),
//       age: parseFloat(document.getElementById("age").value),
//       gender: document.getElementById("gender").value,
//     };

//     const response = await fetch("http://localhost:8000/predict", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify(payload),
//     });

//     const result = await response.json();
//     document.getElementById("output").textContent = JSON.stringify(
//       result,
//       null,
//       2
//     );
//   }
// });

function validateInput(input, regex) {
  var bool = regex.test(input.value);
  input.classList.toggle("is-valid", bool);
  input.classList.toggle("is-invalid", !bool);
  input.nextElementSibling.classList.toggle("d-none", bool);
  return bool;
}

document.getElementById("predictForm").addEventListener("submit", function (e) {
  e.preventDefault();
  if (
    validateInput(
      document.getElementById("weight"),
      /^(30|[3-9][0-9]|1[0-9]{2}|2[0-4][0-9]|250)$/
    ) &&
    validateInput(
      document.getElementById("height"),
      /^(5[0-9]|[6-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/
    ) &&
    validateInput(
      document.getElementById("bmi"),
      /^(1[0-9]|2[0-9]|3[0-9]|4[0-9]|50)(\.\d{1,2})?$/
    ) &&
    validateInput(
      document.getElementById("bodyFat"),
      /^(100(?:\.0{1,2})?|[0-9]{1,2}(?:\.[0-9]{1,2})?)$/
    ) &&
    validateInput(
      document.getElementById("age"),
      /^(?:[1-9]?[0-9]|1[01][0-9]|120)$/
    ) &&
    validateInput(document.getElementById("gender"), /(male|female)/)
  ) {
    // Example dummy response (replace this with your actual fetch/AI call)
    const response = {
      prediction: 2,
      plan: {
        "day 1": {
          optional: "0",
          title: "Full-Body Strength",
          warmup: {
            duration: "5-10",
            exercises: ["dynamic stretching", "light cardio"],
          },
          1: {
            exercise: "Dumbbell Goblet Squats",
            sets: "4",
            reps: "10-12",
          },
          2: { exercise: "Weighted Push-Ups", sets: "4", reps: "8-10" },
          3: { exercise: "Dumbbell Rows", sets: "4", reps: "10-12" },
          4: { exercise: "Lunges", sets: "3", reps: "10-12 (each leg)" },
          6: {
            exercise: "Dumbbell Glute Bridges",
            sets: "3",
            reps: "12-15",
          },
        },
        "day 2": {
          optional: "0",
          title: "Upper Body Strength",
          warmup: {
            duration: "5-10",
            exercises: ["dynamic stretches", "arm circles"],
          },
          1: {
            exercise: "Dumbbell Bench Press",
            sets: "4",
            reps: "10-12",
          },
          2: { exercise: "Lat Pulldown", sets: "4", reps: "10-12" },
          3: {
            exercise: "Barbell Overhead Press",
            sets: "3",
            reps: "10-12",
          },
          4: { exercise: "Bicep Curls", sets: "3", reps: "12-15" },
          5: { exercise: "Tricep Extensions", sets: "3", reps: "12-15" },
          6: {
            exercise: "Inclined Weighted Situps",
            sets: "3",
            reps: "15-20",
          },
        },
        "day 3": {
          optional: "0",
          title: "Lower Body Strength",
          warmup: {
            duration: "5-10",
            exercises: ["dynamic leg swings", "light cardio"],
          },
          1: { exercise: "Barbell Squats", sets: "4", reps: "8-10" },
          2: { exercise: "Deadlifts", sets: "4", reps: "8-10" },
          3: { exercise: "Leg Press", sets: "3", reps: "10-12" },
          4: { exercise: "Hamstring Curls", sets: "3", reps: "10-12" },
          5: { exercise: "Calf Raises", sets: "4", reps: "15-20" },
        },
        "day 4": {
          optional: "0",
          title: "Full Body Strength & Conditioning",
          warmup: {
            duration: "5-10",
            exercises: ["dynamic stretches", "full-body movements"],
          },
          1: { exercise: "Kettlebell Swings", sets: "4", reps: "10-15" },
          2: {
            exercise: "Dumbbell Bench Press",
            sets: "4",
            reps: "8-12",
          },
          3: { exercise: "Barbell Rows", sets: "4", reps: "8-12" },
          4: {
            exercise: "Dumbbell Goblet Squats",
            sets: "4",
            reps: "10-12",
          },
          5: { exercise: "Face Pulls", sets: "3", reps: "15" },
        },
      },
    };

    localStorage.setItem("fitnessPlan", JSON.stringify(response));
    window.location.href = "plan.html"; // redirect to output page
  }
});
