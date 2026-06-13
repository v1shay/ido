<div align="center">

<img width="900" alt="ido banner" src="https://github.com/user-attachments/assets/e5ff1f2a-acd8-4346-b54e-0975422f28e8" />

### The universal agent harness for 3D Design • 3rd Place at AWS x Anthropic Harness Engineering Hack

<br>

<img width="650" alt="ido demo" src="https://github.com/user-attachments/assets/e8a34511-fdf2-494f-89cc-36b95c4b9948" />

</div>

</div>

### what people are building with Ido for Blender →

<div align="center">

<img width="250" height="180" alt="Blender example 1" src="https://github.com/user-attachments/assets/5f72c99c-3a76-468f-bc2a-bb1b90be6ee4" />
<img width="250" height="180" alt="Blender example 2" src="https://github.com/user-attachments/assets/8f5882c3-5b7b-4215-8570-3f92b770a80a" />
<img width="250" height="180" alt="Blender example 3" src="https://github.com/user-attachments/assets/c66922c6-7f37-4a65-a8e5-dca2d4932d61" />

<br />

<img width="250" height="180" alt="Blender example 4" src="https://github.com/user-attachments/assets/df3ee458-9054-4fe1-8faa-800ea297b2fe" />
<img width="250" height="180" alt="Blender example 5" src="https://github.com/user-attachments/assets/eb0bbbdb-11b8-4aa0-81a2-8f7c13969def" />
<img width="250" height="180" alt="Blender example 6" src="https://github.com/user-attachments/assets/77d1dd88-31de-407f-9e5e-9ca6952ea720" />

</div>

### what people are building with Ido for OpenSCAD →

<div align="center">

<img width="240" height="95" alt="Screenshot 1" src="https://github.com/user-attachments/assets/03db51fc-6078-4540-b222-e7c755b9f0c5" />
<img width="240" height="95" alt="Screenshot 2" src="https://github.com/user-attachments/assets/6667fa06-53ac-482e-b1b0-e139b23ec3f7" />
<img width="240" height="95" alt="Screenshot 3" src="https://github.com/user-attachments/assets/fb9c25d0-fa6d-4c33-ab96-754c01ead670" />

<br />

<img width="240" height="95" alt="Screenshot 4" src="https://github.com/user-attachments/assets/6b6cb0bc-1d8a-4242-9340-381603d0d174" />
<img width="240" height="95" alt="Screenshot 5" src="https://github.com/user-attachments/assets/86f080fa-56e8-49bf-b114-af71a10863be" />
<img width="240" height="95" alt="Screenshot 6" src="https://github.com/user-attachments/assets/f076383e-971f-449d-bb45-671ff027b03c" />

<br />

<img width="240" height="95" alt="Screenshot 7" src="https://github.com/user-attachments/assets/71364a6f-7bea-4fab-8d21-7a9b4a84ee36" />
<img width="240" height="95" alt="Screenshot 8" src="https://github.com/user-attachments/assets/1ac1c257-11b1-431c-af56-19b0d9363a85" />
<img width="240" height="95" alt="Screenshot 9" src="https://github.com/user-attachments/assets/c99bf2fb-e996-4136-ad2c-fb40a4329a1e" />

</div>

<br>

<table>
  <tr>
    <td width="42%" valign="middle">
      <img width="666" alt="ido screenshot" src="https://github.com/user-attachments/assets/7e3ac19f-d885-442f-80b1-9f965e81903b" />
    </td>
    <td width="58%" valign="middle">
      <h2>idō pet</h2>
      <p>
        the idō pet allows you to track idō's task progress while working in another tab or viewing results in your modeling software
      </p>
    </td>
  </tr>
</table>

</br>

<details>
<summary><strong>Install</strong></summary>

Requires Python 3.11+ and an `OPENAI_API_KEY`

```bash
git clone https://github.com/v1shay/ido3d
cd ido3D

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"

export OPENAI_API_KEY=sk-...
ido
```

Open `http://127.0.0.1:8010`.

</details>

<details>
<summary><strong>Blender setup</strong></summary>

```bash
cd adapters/blender
zip -r ../../ido_blender.zip ido_blender
cd ../..

ido serve
```

In Blender:

1. Open `Edit -> Preferences -> Add-ons`
2. Install `ido_blender.zip`
3. Press `N` in the 3D View
4. Open the `idō` tab
5. Use `http://127.0.0.1:8010` as the backend

Prompt from the CLI:

```bash
ido prompt --tool blender "make a small cabin"
```

</details>

<details>
<summary><strong>OpenSCAD setup</strong></summary>

Install OpenSCAD and make sure `openscad` is on your `PATH`

```bash
ido open openscad
ido prompt --tool openscad "make a bracket with two mounting holes"
```

Outputs are written to `~/.ido/projects/default`

</details>

<details>
<summary><strong>Command</strong></summary>

```bash
ido                 # open the local app
ido serve           # run the API
ido status          # check runtime status
ido reset           # clear generated files
```

</details>
