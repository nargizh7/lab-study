# Task Manager

This is a web-based task management application where users can create accounts, manage to-do tasks, upload profile images, and change their passwords. The application runs locally and you interact with it through your web browser.

---

## Your Goal

This application has bugs. Your goal is to make **every feature work correctly** by finding and fixing the issues with the help of an AI coding assistant (Claude). Work through the features in the order listed below.

---

## Setup

You need two terminal windows open side by side, plus your web browser.

### Terminal 1 — Start the application server

```bash
cd ~/task-manager
source venv/bin/activate
python app.py
```

You should see output like this:

```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

**Leave this terminal running.** The server must stay running while you work. Do not close it or press Ctrl+C.

If the server crashes or stops responding at any point, restart it:

```bash
python app.py
```

### Terminal 2 — Start the AI assistant

Open a **new terminal tab or window**, then run:

```bash
cd ~/task-manager
source venv/bin/activate
claude
```

This starts the Claude AI assistant. You can describe problems to it in plain English and it will help you fix them. 

### Browser

Open **http://127.0.0.1:5000** in your web browser. You should see the Task Manager welcome screen.

If you see an error page instead of the welcome screen, that is one of the bugs you will need to fix. Describe what you see to Claude.

---

## How to Work Through the Task

1. Try each feature below **in order** in the browser
2. If it works as described, move to the next feature
3. If something does not work — you see an error, nothing happens, or the result is wrong — describe what you tried and what went wrong to Claude in Terminal 2
4. After Claude makes a fix, refresh the browser and try the feature again
5. If the server needs to restart, Claude will handle that — you may need to refresh the browser page afterward

Some features depend on earlier ones. For example, you cannot create tasks until you have registered and logged in. Follow the order.

---

## Features to Test

### 1. Create an Account

On the welcome screen, select the **Register** tab. Enter a username and password, then click **Create Account**.

**Expected:** A green notification appears confirming your account was created.

**If broken:** You may see an error message or nothing happens. Tell Claude.

---

### 2. Log In

Switch to the **Login** tab. Enter the username and password you just registered with, then click **Log In**.

**Expected:** The page changes to show your personal dashboard with a Profile section at the top and a My Tasks section below.

**If broken:** You might see "Invalid credentials" even with correct information, or an error page. Tell Claude exactly what happens.

**Note:** If the database was reset during a fix, you may need to register a new account.

---

### 3. Add a Task

In the **My Tasks** section, type a task title (and optionally a description), then click **Add**.

**Expected:** Your task appears in the list below the form.

**If broken:** The task may not appear or you may see an error. Tell Claude.

---

### 4. View Your Tasks

After adding tasks, they should appear in your task list with action buttons: a green checkmark, a pencil, and a red X.

**Expected:** All tasks you created are listed with their action buttons.

**If broken:** The list may be empty, show errors, or not load. Tell Claude.

---

### 5. Mark a Task as Complete

Click the **green checkmark button** on any task.

**Expected:** The task becomes grayed out and shows a "Done" badge.

**If broken:** Nothing may happen or you may see an error. Tell Claude.

---

### 6. Edit a Task

Click the **pencil button** on any task.

**Expected:** A popup dialog appears. Change the title or description, click **Save Changes**, and the task list updates.

**If broken:** The popup may not appear, the save may fail, or changes may not show. Tell Claude.

---

### 7. Delete a Task

Click the **red X button** on any task.

**Expected:** The task disappears from the list.

**If broken:** The task may remain or you may see an error. Tell Claude.

---

### 8. Upload a Profile Image

In the **Profile** section at the top of your dashboard, click the file chooser and select **only** the file named `cmu tartan.jpeg` located in your **Documents** folder (`~/Documents/cmu tartan.jpeg`). Do not use any other file for this test. Then click **Upload**.

**Expected:** Your profile avatar updates to show the `cmu tartan.jpeg` image.


**If broken:** You may see an error or the image may not appear. Tell Claude.

---

### 9. Change Your Password

In the Profile section, click **Change Password**. Enter your current password and a new password, then click **Update**.

**Expected:** A green confirmation appears. You can verify by refreshing the page (which logs you out) and logging in with your new password.

**If broken:** You may see an error, or the change may appear to succeed but the new password does not work. Tell Claude the full situation.

---

## Notes

- **You can always re-test.** After a fix, go back and re-test the feature to make sure it actually works.
- **If the server crashes**, restart it with `python app.py` in Terminal 1 and refresh the browser.
- **You do not need to edit any code yourself.** Claude can make all code changes for you