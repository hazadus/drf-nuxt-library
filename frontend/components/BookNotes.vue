<template>
  <div class="box">
    <!-- Main Level container -->
    <nav class="level">
      <!-- Left side -->
      <div class="level-left">
        <div class="level-item">
          <span class="icon-text">
            <span class="icon">
              <Icon name="mdi:notebook" />
            </span>
            <span>
              <b>
                Заметки к книге
              </b>
            </span>
          </span>
        </div>
      </div>

      <!-- Right side -->
      <div class="level-right">
        <button class="button">
          <span class="icon">
            <Icon name="mdi:note-edit-outline" />
          </span>
          <span>
            Написать заметку
          </span>
        </button>

        <button v-if="false" class="button is-primary is-loading">Loading</button>
      </div>
    </nav>
  </div>
</template>