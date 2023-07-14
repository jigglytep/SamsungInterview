# SamsungInterview

    getEmail
        parseSubject, parseBody
      new:
        create event in db
        download test -> DB update
      change:
        update event in db
        send db notification
      delete:
        mark event:
            jobState "failed"
            status cancelled
    due_date:
        star_submission() -> P/F db update
        sets as IDL
