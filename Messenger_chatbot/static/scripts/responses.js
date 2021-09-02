function getBotResponse(input) {
    //rock paper scissors
    if (input == "Hi" || input == "hi" || input == "Hey") {
        return "Hi there! How can I help you today?";
    } else if (input == "Need some help.") {
        return "Yes, how can I assist you on your Cloud journey?";
    } else if (input == "bye" || input =="Bye") {
        return "Sad to see you go :(";
    }

    // Simple responses
    if (input == "hello") {
        return "Hello there!";
    } else if (input == "goodbye") {
        return "Talk to you later!";
    } else {
        return "Sorry I don't understand. Please try to ask me something else.";
    }
}