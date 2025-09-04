# Composables

This directory houses reusable Vue composable functions.

## useTeamColors

`useTeamColors(nameRef)` returns a reactive style object containing CSS
variables for a team's primary, secondary and accent colors. Pass a team name
or a ref to one and use the returned object to theme components based on the
selected team.
