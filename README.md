# GMail Inbox Manager

Command-line interface to manage a cluttered mailbox.

## Code Example
First, get you some credentials [here](https://developers.google.com/identity/protocols/OAuth2).
> Copy your new creds into a file `credentials.json`, in the `inbox_manager` package.

Then just import the package, construct a manager, and pass a target label to `remove`. (Python 3 is required)
```python
from inbox_manager import InboxManager

mgr = InboxManager()
mgr.remove('UNREAD')
```

## Installation
```sh
git clone https://github.com/parkerduckworth/inbox-manager.git
```

## Other Useful Information
Some common labels:
 - UNREAD
 - SPAM
 - CATEGORY_(YOUR CATEGORY) ex. CATEGORY_PROMOTIONS
