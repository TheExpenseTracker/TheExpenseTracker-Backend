const list = document.getElementById("list");
const balance = document.getElementById("balance");
const money_plus = document.getElementById("money-plus");
const money_minus = document.getElementById("money-minus");
const saving1 = document.getElementById("saving");
let transactions = [];

fetch(/history/)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(userData => {
    console.log('User Data:', userData);
    // Process the retrieved user data
    userData.forEach(transaction => {
      const sign = transaction.amount < 0 ? "-" : "+";
      const item = document.createElement("li");
      const timestamp = Date.now();
      item.dataset.timestamp = timestamp; // Store the timestamp as a data attribute

      //Add Class Based on Value
      item.classList.add(transaction.amount < 0 ? "minus" : "plus");
      item.id=transaction.id;
      item.innerHTML = `
        ${transaction.text} <span>${sign}${Math.abs(transaction.amount)}</span>
        <button class="delete-btn" onclick="removeTransaction(${
          transaction.id
        })">x</button>
        `;
      list.appendChild(item);
      });
  })
  .catch(error => {
    console.error('Error:', error);
  });

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function addTransaction() {
  // e.preventDefault();
  if (text.value.trim() === "" || amount.value.trim() === "") {
    alert("please add text and amount");
  } else {
    const transaction = {
      // id:generateID(),
      text: text.value,
      amount: +amount.value,
      
    };
    fetch("/transaction/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
        "X-SessionID": getCookie("sessionid"),
      },
      body: JSON.stringify(transaction),
    })
      .then((response) => response.json())
      .then((data) => {
        // Update the balance based on the response
       
        balance.innerText = `$${data.balance}`;
        money_plus.innerText = `$${data.income}`;
        money_minus.innerText = `$${data.expense}`;
        saving1.innerText = `$${data.svg_amt}`;
        // saving_goal.innerText = `$${data.saving}`;
        

        // Reset form values
        
        // Update the transaction list
        transactions.push(data.transaction);
        
        addTransactionDOM(data.transaction);
        // Init();
        updateLocalStorage();
        text.value = "";
        amount.value = "";
      })
      .catch((error) => {
        console.error("Error:", error);
      });
      fetch('/update_chvalues/')
      .then(response => response.json())
      .then(data => {
          
          expenseAndIncomeChart.data.datasets[0].data = data.e;
          expenseAndIncomeChart.data.datasets[1].data = data.i;
          expenseAndIncomeChart.data.labels = data.c;
          expenseAndIncomeChart.update();
          // expensebycategory.data.labels = data.c;
          
          expensebycategory.data.datasets[0].data = data.e;
          expensebycategory.data.labels = data.te;
          expensebycategory.update();
          
          dates = data.c;
          expenses = data.e;
          
      })
        
      .catch(error => {
          console.error('Error fetching data:', error);
     });
  
  fetch("/prediction/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
      "X-SessionID": getCookie("sessionid"),
    },
    body: JSON.stringify(transaction),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data.message) {
        alert(data.message);
      } else {
        console.log("Message is null or undefined");
      }

    })
    .catch((error) => {
      console.error("Error:", error);
    });
  
    
  return false;
  }
}

//5.5
//Generate Random ID
function generateID() {
  return Math.floor(Math.random() * 1000000000);
}

//2

//Add Trasactions to DOM list
function addTransactionDOM(transaction) {
  //GET sign
  const sign = transaction.amount < 0 ? "-" : "+";
  const item = document.createElement("li");
  const timestamp = Date.now();
  item.dataset.timestamp = timestamp; // Store the timestamp as a data attribute

  //Add Class Based on Value
  item.classList.add(transaction.amount < 0 ? "minus" : "plus");
  item.id=transaction.id;
  item.innerHTML = `
    ${transaction.text} <span>${sign}${Math.abs(transaction.amount)}</span>
    <button class="delete-btn" onclick="removeTransaction(${
      transaction.id
    })">x</button>
    `;
  list.appendChild(item);
  // Store the timestamp in localStorage
  localStorage.setItem(`transaction-${transaction.id}-timestamp`, timestamp); // 24 hours in milliseconds
}


// Update the balance income and expence
// function updateValues() {
//   const amounts = transactions.map((transaction) => transaction.amount);
//   const total = amounts.reduce((acc, item) => (acc += item), 0).toFixed(2);
//   const income = amounts
//     .filter((item) => item > 0)
//     .reduce((acc, item) => (acc += item), 0)
//     .toFixed(2);
//   const expense = (
//     amounts.filter((item) => item < 0).reduce((acc, item) => (acc += item), 0) *
//     -1
//   ).toFixed(2);

//   balance.innerText = `$${total}`;
//   money_plus.innerText = `$${income}`;
//   money_minus.innerText = `$${expense}`;
// }
// let selectedId = null;

// function handleIncomeSourceChange(event) {
//   selectedId = event.target.value;
//   updateValues();
// }



// function updateValues() {
//   console.log("Verified")
//   fetch("/initial_data/")
//     .then((response) => response.json())
//     .then((data) => {
//       const { income_sources, expenses } = data;
//       const selectedIncomeSource = income_sources.find(
//         (source) => source.id == selectedId
//       );
//       let selectedIncome = selectedIncomeSource
//         ? selectedIncomeSource.amount
//         : 0;
//       selectedIncome = Number(selectedIncome);
//       console.log(selectedIncome);

//       const totalIncome = income_sources.reduce(
//         (acc, source) => acc + source.amount,
//         0
//       );
//       const totalExpense = expenses.reduce(
//         (acc, expense) => acc + expense.amount,
//         0
//       );
//       console.log(totalExpense);

//       balance.innerText = `$${(selectedIncome - totalExpense).toFixed(2)}`;
//       money_plus.innerText = `$${selectedIncome.toFixed(2)}`;
//       money_minus.innerText = `$${totalExpense.toFixed(2)}`;
//       fetch("/updated_values/", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//           "X-CSRFToken": getCookie("csrftoken"), // Use your function to get the CSRF token
//         },
//         body: JSON.stringify({
//           selectedIncome: selectedIncome,
//           totalIncome: totalIncome,
//           totalExpense: totalExpense,
//         }),
//       })
//         .then((response) => response.json())
//         .then((data) => {
//           console.log("Values updated successfully in Django");
//         })
//         .catch((error) => {
//           console.error("Error updating values in Django:", error);
//         });
//     })
//     .catch((error) => {
//       console.error("Error:", error);
//     });
// }

//Remove Transaction by ID
function removeTransaction(id) {
  fetch(`/remove_transaction/${id}/`)
        .then(response =>  response.json()) // Read the response as text
           
        .then(data => {
            // Update the transactions array and localStorage
            balance.innerText = `$${data.balance}`;
            money_plus.innerText = `$${data.income}`;
            money_minus.innerText = `$${data.expense}`;
            updateLocalStorage();
            const transactionElement = document.getElementById(id);
           if (transactionElement) {
             transactionElement.remove();
             }
            // Find and remove the element from the DOM
            
            // Update the charts
            // Init();
        })
        .catch(error => {
          console.error('Error removing transaction:', error);
      });
      
        fetch('/update_chvalues/')
            .then(response => response.json())
            .then(data => {
          
              expenseAndIncomeChart.data.datasets[0].data = data.e;
              expenseAndIncomeChart.data.datasets[1].data = data.i;
              expenseAndIncomeChart.data.labels = data.c;
              expenseAndIncomeChart.update();
              // expensebycategory.data.labels = data.c;
              
              expensebycategory.data.datasets[0].data = data.e;
              expensebycategory.data.labels = data.te;
              expensebycategory.update();
              
              dates = data.c;
              expenses = data.e;
          
      })
      
        
      .catch(error => {
          console.error('Error fetching data:', error);
     });

        
        
}

//last
//update Local Storage Transaction
function updateLocalStorage() {
  localStorage.setItem("transactions", JSON.stringify(transactions));
}

//3

//Init App
function Init() {
  list.innerHTML = "";
  transactions.forEach(addTransactionDOM);
  updateValues();
}

// Init();
document.addEventListener("DOMContentLoaded", function() {
  const oneDayMs = 24 * 60 * 60 * 1000;
  const keys = Object.keys(localStorage);

  keys.forEach((key) => {
    if (key.startsWith("transaction-")) {
      const timestamp = localStorage.getItem(key);
      if (Date.now() - timestamp > oneDayMs) {
        const id = key.split("-")[1];
        const transactionElement = document.getElementById(`transaction-${id}`);
        if (transactionElement) {
          transactionElement.remove();
          localStorage.removeItem(key); // Remove the timestamp from localStorage
        }
      }
    }
  });
});
// form.addEventListener("submit", addTransaction);
// document.querySelector(".btn-add").addEventListener("click", addTransaction);
function generateIncomeFields() {
  var numIncomes = parseInt(document.getElementById("numIncomes").value);
  var incomeContainer = document.getElementById("incomeContainer");
  incomeContainer.innerHTML = "";
  for (var i = 1; i <= numIncomes; i++) {
    incomeContainer.innerHTML += `
      <div>
          <label for="incomeSource${i}">Income Source ${i}:</label>
          <input type="text" id="incomeSource${i}" name="incomeSource${i}" value="{{ s.source }}" required>
          <label for="incomeAmount${i}">Income Amount ${i}:</label>
          <input type="text" id="incomeAmount${i}" name="incomeAmount${i}" value="{{ s.amount }}" required>
      </div>
      `;
  }
  document.getElementById("incomeFields").style.display = "block";
  document.getElementById("submitButton").style.display = "block";
  document.getElementById("nextButton").style.display = "none";
}

function submitForm(event) {
  event.preventDefault();
  
  // Check if the URL contains the show_elements parameter
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has("show_elements")) {
    document.querySelector(".header-main").style.display = "block";
    document.querySelector(".main-content").style.display = "block";
    document.querySelector(".cls1").style.display = "block";
    document.querySelector(".cls2").style.display = "block";
    document.querySelector(".initial-form-container").style.display = "none";
  }
  
  setTimeout(() => {
    document.getElementById("initial-form").submit();
  }, 100);
}
