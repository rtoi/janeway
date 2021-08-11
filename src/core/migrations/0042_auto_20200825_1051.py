# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-08-25 09:51
from __future__ import unicode_literals

from django.db import migrations, IntegrityError, transaction

from core.model_utils import merge_models


def lower_all_usernames(apps, schema_editor):
    Account = apps.get_model('core', 'Account')
    accounts = Account.objects.all()
    handled = set()

    for account in accounts:
        if account.username.lower() in handled:
            continue
        try:
            with transaction.atomic():
                account.username = account.username.lower()
                account.save()
        except IntegrityError:
            same_accounts = Account.objects.filter(username__iexact=account.username)
            handled |= handle_unique_username_violation(same_accounts, apps)

def handle_unique_username_violation(same_accounts, apps):
    AccountRole = apps.get_model('core', 'Accountrole')
    Account = apps.get_model('core', 'Account')
    real_account = None

    # Try checking if one has logged in
    has_logged_in = same_accounts.filter(last_login__isnull=False)
    if has_logged_in.count == 1:
        real_account = has_logged_in[0]

    if real_account is None:
        # Try checking if one account has a non-author role:
        account_roles_ids = AccountRole.objects.filter(
            user__in=same_accounts,
        ).exclude(
            role__slug="author"
        ).values_list("user", flat=True)
        if len(set(account_roles_ids)) == 1:
            real_account = Account.objects.get(id=account_roles_ids[0])

    if real_account is None:
        # Try checking if one account is author
        authors = []
        for acc in same_accounts:
            if acc.article_set.exists():
                authors.append(acc)
        if len(authors) >2:
            raise Exception(
                "Can't workout the real user for username %s" % acc.username)
        elif len(authors) == 1:
            real_account = authors[0]

    if real_account is None:
        # At this point no account is an author, has a role or logged in
        # Declare any of them the real author
        real_account = same_accounts[0]

    merged = set()
    for acc in same_accounts:
        if acc != real_account:
            merge_models(acc, real_account)
            merged.add(acc.username.lower())
    real_account.username = real_account.username.lower()
    real_account.save()
    return merged






class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_fix_reminder_name_description'),
    ]

    operations = [
        migrations.RunPython(
            lower_all_usernames,
            reverse_code=migrations.RunPython.noop,
            atomic=False,
        ),
    ]
