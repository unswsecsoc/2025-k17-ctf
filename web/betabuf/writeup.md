## betabuf
```
We regret telling the intern about Protocol Buffers. Hopefully they'll clean things up before we leave closed beta.
```

## rough writeup
1. the invite has no signature, so you can use something like https://www.protobufpal.com/ to forge an invite
2. protobuf keeps unknown fields, so we can smuggle an `is_verified = true` into the registration message through the registrationInvite

=> these 2 steps give an invite of `38ffff83fea6dee1114001`

3. the truncation then concatenation in `/rename` allows you to corrupt the message and make it interpret data as fields.
by playing around with https://protobuf-decoder.netlify.app/ you can find the required length (985 bytes) of username to make the truncation essentially delete the 2 byte tag of the next field. if you then rename to "\u0018\u0001\u0020\u0001", this data will be interpreted as a message and you'll get an admin account token
4. for the SecureConnectionDetails, it's a type confusion vulnerability with a HighScore message (the type isn't checked so you can use a HighScore with score = 1 as a SecureConnectionDetails message)