# [Chuck LePlant](https://chuckleplant.github.io/)

## Setting up

* Install ruby
* Install python
* `git submodule update --init`
* `gem install bundler`
* `bundle add jekyll`
* `python -m pip install --upgrade pip`

## Python requirements

* Pillow
* piexif
* pyyaml

## Running locally

* Create `_config_private.yml` (ignored by git) for secrets:
  ```yaml
  google_maps_api_key: "YOUR_KEY"
  google_maps_map_id: "YOUR_MAP_ID"
  ```
* Serve the site with both configs so the private values are picked up:
  ```
  bundle exec jekyll serve --config _config.yml,_config_private.yml
  ```
