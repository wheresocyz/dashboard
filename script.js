// Mock items
const items = ["Default Outfit", "Default Pickaxe", "Default Glider", "Default Emote"];

// Mock party members
const partyMembers = [
  { name: "Bricked Weenie", level: 1 },
  { name: "Player2", level: 1 },
  { name: "Player3", level: 1 }
];

// Render items
const itemsList = document.getElementById("items-list");
if (itemsList) {
  items.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    itemsList.appendChild(li);
  });
}

// Render party members
const partyList = document.getElementById("party-list");
if (partyList) {
  partyMembers.forEach(member => {
    const li = document.createElement("li");
    li.textContent = `${member.name} (Level ${member.level})`;
    partyList.appendChild(li);
  });
}

// Custom status
const statusInput = document.getElementById("status-msg");
const setStatusBtn = document.getElementById("set-status");
const currentStatus = document.getElementById("current-status");

if (setStatusBtn) {
  setStatusBtn.addEventListener("click", () => {
    currentStatus.textContent = statusInput.value || "None";
    statusInput.value = "";
  });
}
