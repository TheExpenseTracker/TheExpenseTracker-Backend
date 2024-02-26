const list = document.getElementById("list");
const balance = document.getElementById("balance");
const money_plus = document.getElementById("money-plus");
const money_minus = document.getElementById("money-minus");
let transactions = [];

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function generateID() {
  return Math.floor(Math.random() * 1000000000);
}

function addTransactionDOM(transaction) {
  const sign = transaction.amount < 0 ? "-" : "+";
  const item = document.createElement("li");
  item.classList.add(transaction.amount < 0 ? "minus" : "plus");
  item.innerHTML = `
    ${transaction.text} <span>${sign}${Math.abs(transaction.amount)}</span>
    <button class="delete-btn" onclick="removeTransaction(${
      transaction.id
    })">x</button>
    `;
  list.appendChild(item);
}

let selectedId = null;

function handleIncomeSourceChange(event) {
  selectedId = event.target.value;
  updateValues();
}

document
  .getElementById("income_source")
  .addEventListener("change", handleIncomeSourceChange);


function updateValues() {
  console.log("Verifying data...");

  if (!initialDataReceived && totalExpense === 0 && totalIncome === 0) {
    fetch("/initial_data/")
      .then((response) => response.json())
      .then((data) => {
        const { income_sources, expenses } = data;
        totalIncome = income_sources.reduce(
          (acc, source) => acc + source.amount,
          0
        );
        totalExpense = expenses.reduce((acc, expense) => acc + expense.amount, 0);
        initialDataReceived = true;
        updateUI();
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  } else {
    updateUI();
  }
}

function updateUI() {
  console.log("Updating UI...");

  const moneyPlusElement = document.getElementById("money-plus");
  const moneyMinusElement = document.getElementById("money-minus");

  if (moneyPlusElement && moneyMinusElement) {
    moneyPlusElement.innerText = `$${totalIncome.toFixed(2)}`;
    moneyMinusElement.innerText = `-$${totalExpense.toFixed(2)}`;
  } else {
    console.error("Error: Unable to find elements with IDs 'money-plus' or 'money-minus'");
  }

  console.log("Sending updated values to Django...");
  fetch("/updated_values/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      selectedIncome: totalIncome,
      totalIncome: totalIncome,
      totalExpense: totalExpense,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Values updated successfully in Django");
    })
    .catch((error) => {
      console.error("Error updating values in Django:", error);
    });
}

function addTransaction() {
  if (text.value.trim() === "" || amount.value.trim() === "") {
    alert("Please add text and amount");
  } else {
    const transaction = {
      text: text.value,
      amount: +amount.value,
      income_source_id: document.getElementById("income_source").value,
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
        transactions.push(data.transaction);
        addTransactionDOM(data.transaction);
        updateUI(); // Call updateValues() after adding a new transaction
        updateLocalStorage();
        text.value = "";
        amount.value = "";
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
  return false;
}


function removeTransaction(id) {
  transactions = transactions.filter((transaction) => transaction.id !== id);
  updateLocalStorage();
  Init();
}

function updateLocalStorage() {
  localStorage.setItem("transactions", JSON.stringify(transactions));
}

function Init() {
  list.innerHTML = "";
  transactions.forEach(addTransactionDOM);
  updateValues();
}

function generateIncomeFields() {
  var numIncomes = parseInt(document.getElementById("numIncomes").value);
  var incomeContainer = document.getElementById("incomeContainer");
  incomeContainer.innerHTML = "";
  for (var i = 1; i <= numIncomes; i++) {
    incomeContainer.innerHTML += `
      <div>
          <label for="incomeSource${i}">Income Source ${i}:</label>
          <input type="text" id="incomeSource${i}" name="incomeSource${i}" required>
          <label for="incomeAmount${i}">Income Amount ${i}:</label>
          <input type="text" id="incomeAmount${i}" name="incomeAmount${i}" required>
      </div>
      `;
  }
  document.getElementById("incomeFields").style.display = "block";
  document.getElementById("submitButton").style.display = "block";
  document.getElementById("nextButton").style.display = "none";
}

function submitForm(event) {
  event.preventDefault();
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has("show_elements")) {
    document.querySelector(".header-main").style.display = "block";
    document.querySelector(".main-content").style.display = "block";
    document.querySelector(".initial-form-container").style.display = "none";
  }

  setTimeout(() => {
    document.getElementById("initial-form").submit();
  }, 100);
}

// Initialization
Init();
