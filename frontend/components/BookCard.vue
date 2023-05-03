<template>
  <div class="box">
    <!-- Main Level container -->
    <nav class="level">
      <!-- Left side -->
      <div class="level-left">
        <div class="level-item">
          <span class="icon-text">
            <span class="icon">
              <Icon name="mdi:bookshelf" />
            </span>
            <span>
              <b>
                Ваши книги
              </b>
            </span>
            <span class="has-text-grey">
              &middot; Добавлена
            </span>
          </span>
        </div>
      </div>

      <!-- Right side -->
      <div class="level-right">
        <button class="button">
          <span class="icon">
            <Icon name="mdi:book-plus" />
          </span>
          <span>
            Добавить
          </span>
        </button>

        <button class="button">
          <span class="icon">
            <Icon name="mdi:book-minus" />
          </span>
          <span>
            Убрать
          </span>
        </button>

        <button class="button is-primary is-loading">Loading</button>
      </div>
    </nav>

    <div class="field">
      <div class="control">
        <label class="checkbox mr-2">
          <input type="checkbox">
          Избранная
        </label>
        <label class="checkbox mr-2">
          <input type="checkbox">
          Хочу прочитать
        </label>
        <label class="checkbox mr-2">
          <input type="checkbox">
          Читаю
        </label>
        <label class="checkbox">
          <input type="checkbox">
          Прочитал
        </label>
      </div>
    </div>
  </div>
</template>