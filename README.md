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


<h2>📚 Protocol Grammar</h2>
<pre>
&lt;mail-from-cmd&gt; → “MAIL” &lt;whitespace&gt; “FROM:” &lt;nullspace&gt; &lt;reverse-path&gt;
&lt;nullspace&gt; → &lt;null&gt; | &lt;whitespace&gt;
&lt;whitespace&gt; → &lt;SP&gt; | &lt;SP&gt; &lt;whitespace&gt;
&lt;SP&gt; → " " | "\t" /* the space or tab character */
&lt;null&gt; → no character
&lt;reverse-path&gt; → &lt;path&gt;
&lt;path&gt; → "&lt;" &lt;mailbox&gt; "&gt;"
&lt;mailbox&gt; → &lt;local-part&gt; "@" &lt;domain&gt;
&lt;local-part&gt; → &lt;string&gt;
&lt;string&gt; → &lt;char&gt;+ 
&lt;char&gt; → any one of the printable ASCII characters, but not any of &lt;special&gt; or &lt;SP&gt;
&lt;domain&gt; → &lt;element&gt; | &lt;element&gt; "." &lt;domain&gt;
&lt;element&gt; → &lt;letter&gt; | &lt;name&gt;
&lt;name&gt; → &lt;letter&gt; &lt;let-dig-str&gt;
&lt;letter&gt; → any one of the 52 alphabetic characters A-Z or a-z
&lt;let-dig-str&gt; → &lt;let-dig&gt;+ 
&lt;let-dig&gt; → &lt;letter&gt; | &lt;digit&gt;
&lt;digit&gt; → "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
&lt;CRLF&gt; → "\n" /* the newline character */
&lt;special&gt; → "&lt;" | "&gt;" | "(" | ")" | "[" | "]" | "\\" | "." | "," | ";" | ":" | "@" | "&quot;"
<br>
&lt;rcpt-to-cmd&gt; → “RCPT” &lt;whitespace&gt; “TO:” &lt;nullspace&gt; &lt;forward-path&gt;
&lt;nullspace&gt; → &lt;CRLF&gt;
&lt;forward-path&gt; → &lt;path&gt;
<br>
&lt;data-cmd&gt; → “DATA” &lt;nullspace&gt; &lt;CRLF&gt;
</pre>


<h2>📦 Requirements</h2>
<ul>
    <li>Python 3.x</li>
</ul>



</body>
</html>
