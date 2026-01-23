<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>SMTP-Parser</h1>

<p>A command‑line parser for the <strong>Simple Mail Transfer Protocol (SMTP)</strong> that reads SMTP client commands and ensures they follow the correct syntax and sequence.</p>

<p>SMTP is the protocol used by email clients and servers to <strong>send email messages</strong> across the internet.</p>

<h2>🚀 Features</h2>
<ul>
    <li>Parses SMTP commands such as <code>MAIL FROM</code>, <code>RCPT TO</code>, and <code>DATA</code></li>
    <li>Implements <strong>recursive descent parsing</strong> to process commands according to protocol grammar</li>
    <li>Uses a <strong>state machine</strong> to enforce correct command order</li>
    <li>Detects malformed commands and invalid protocol transitions</li>
    <li>Helps validate SMTP input for testing or educational use</li>
</ul>

<h2>🛠️ How It Works</h2>
<p>This parser uses <strong>recursive descent parsing</strong> to analyze SMTP commands and tracks the connection state using a state machine. Commands that don’t match the expected syntax or sequence are rejected.</p>

<h2>📦 Requirements</h2>
<ul>
    <li>Python 3.x</li>
</ul>

</body>
</html>
